import os
import git
from typing import Dict, Any, List
from datetime import datetime
from app.services.scanner.dependency_parser import DependencyParser

class GitScanner:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def scan(self) -> Dict[str, Any]:
        result = {
            "metadata": {},
            "commits": [],
            "branches": [],
            "tags": [],
            "files": [],
            "dependencies": [],
            "docs": []
        }
        
        # Git Metadata & Commits
        if os.path.exists(os.path.join(self.repo_path, ".git")):
            try:
                repo = git.Repo(self.repo_path)
                result["metadata"]["active_branch"] = str(repo.active_branch) if not repo.head.is_detached else "detached"
                result["branches"] = [b.name for b in repo.branches]
                result["tags"] = [t.name for t in repo.tags]
                
                for commit in list(repo.iter_commits(max_count=200)):
                    result["commits"].append({
                        "hash": commit.hexsha,
                        "author_name": commit.author.name,
                        "author_email": commit.author.email,
                        "commit_date": datetime.fromtimestamp(commit.committed_date),
                        "message": commit.message.strip()
                    })
            except Exception as e:
                print(f"Git reading warning: {e}")

        # Directory Scan
        for root, dirs, files in os.walk(self.repo_path):
            if ".git" in root or "node_modules" in root or "venv" in root or "__pycache__" in root or "dist" in root:
                continue
            for f in files:
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, self.repo_path)
                ext = os.path.splitext(f)[1].lower()
                
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as file_obj:
                        content = file_obj.read()
                except Exception:
                    content = ""

                line_count = len(content.splitlines()) if content else 0
                size = os.path.getsize(full_path)

                # Track documentation
                if f.lower().startswith("readme") or ext in [".md", ".rst", ".txt"]:
                    result["docs"].append({"path": rel_path, "content": content})

                # Track dependency files
                if f == "package.json":
                    deps = DependencyParser.parse_package_json(content)
                    for d in deps: d["source_file"] = rel_path
                    result["dependencies"].extend(deps)
                elif f == "pyproject.toml":
                    deps = DependencyParser.parse_pyproject_toml(content)
                    for d in deps: d["source_file"] = rel_path
                    result["dependencies"].extend(deps)
                elif f == "requirements.txt":
                    deps = DependencyParser.parse_requirements_txt(content)
                    for d in deps: d["source_file"] = rel_path
                    result["dependencies"].extend(deps)
                elif f == "Cargo.toml":
                    deps = DependencyParser.parse_cargo_toml(content)
                    for d in deps: d["source_file"] = rel_path
                    result["dependencies"].extend(deps)
                elif f == "go.mod":
                    deps = DependencyParser.parse_go_mod(content)
                    for d in deps: d["source_file"] = rel_path
                    result["dependencies"].extend(deps)

                lang = self._detect_language(f)
                result["files"].append({
                    "path": rel_path,
                    "language": lang,
                    "size": size,
                    "line_count": line_count,
                    "content": content
                })

        return result

    def _detect_language(self, filename: str) -> str:
        ext = os.path.splitext(filename)[1].lower()
        mapping = {
            ".py": "python",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".js": "javascript",
            ".jsx": "javascript",
            ".md": "markdown",
            ".json": "json",
            ".toml": "toml",
            ".rs": "rust",
            ".go": "go",
            ".html": "html",
            ".css": "css"
        }
        return mapping.get(ext, "text")
