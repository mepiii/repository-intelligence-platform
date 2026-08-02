import json
import tomllib
import re
from typing import List, Dict, Any

class DependencyParser:
    @staticmethod
    def parse_package_json(content: str) -> List[Dict[str, Any]]:
        deps = []
        try:
            data = json.loads(content)
            for name, ver in data.get("dependencies", {}).items():
                deps.append({"name": name, "version": ver, "type": "runtime"})
            for name, ver in data.get("devDependencies", {}).items():
                deps.append({"name": name, "version": ver, "type": "dev"})
        except Exception:
            pass
        return deps

    @staticmethod
    def parse_pyproject_toml(content: str) -> List[Dict[str, Any]]:
        deps = []
        try:
            data = tomllib.loads(content)
            project_deps = data.get("project", {}).get("dependencies", [])
            for dep in project_deps:
                match = re.match(r"^([a-zA-Z0-9_\-\.]+)(.*)$", dep.strip())
                if match:
                    deps.append({"name": match.group(1), "version": match.group(2).strip(), "type": "runtime"})
        except Exception:
            pass
        return deps

    @staticmethod
    def parse_requirements_txt(content: str) -> List[Dict[str, Any]]:
        deps = []
        for line in content.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                parts = re.split(r"==|>=|<=|~=", line)
                name = parts[0].strip()
                ver = parts[1].strip() if len(parts) > 1 else "*"
                deps.append({"name": name, "version": ver, "type": "runtime"})
        return deps

    @staticmethod
    def parse_cargo_toml(content: str) -> List[Dict[str, Any]]:
        deps = []
        try:
            data = tomllib.loads(content)
            for name, ver in data.get("dependencies", {}).items():
                v_str = ver if isinstance(ver, str) else ver.get("version", "*")
                deps.append({"name": name, "version": v_str, "type": "runtime"})
        except Exception:
            pass
        return deps

    @staticmethod
    def parse_go_mod(content: str) -> List[Dict[str, Any]]:
        deps = []
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("require") or (" " in line and not line.startswith("module") and not line.startswith("go ")):
                parts = line.replace("require", "").strip().split()
                if len(parts) >= 2:
                    deps.append({"name": parts[0], "version": parts[1], "type": "runtime"})
        return deps
