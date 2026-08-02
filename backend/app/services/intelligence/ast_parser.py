import ast
import re
from typing import List, Dict, Any

class ASTParser:
    @staticmethod
    def parse_python(code: str, file_path: str = "") -> Dict[str, Any]:
        symbols = []
        imports = []
        docstrings = []
        
        try:
            tree = ast.parse(code)
            module_doc = ast.get_docstring(tree)
            if module_doc:
                docstrings.append({"type": "module", "docstring": module_doc, "line": 1})

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                    f_doc = ast.get_docstring(node)
                    args = [a.arg for a in node.args.args]
                    sig = f"{node.name}({', '.join(args)})"
                    symbols.append({
                        "name": node.name,
                        "kind": "function",
                        "start_line": node.lineno,
                        "end_line": getattr(node, "end_lineno", node.lineno),
                        "docstring": f_doc,
                        "signature": sig
                    })
                elif isinstance(node, ast.ClassDef):
                    c_doc = ast.get_docstring(node)
                    bases = [b.id for b in node.bases if isinstance(b, ast.Name)]
                    sig = f"class {node.name}({', '.join(bases)})"
                    symbols.append({
                        "name": node.name,
                        "kind": "class",
                        "start_line": node.lineno,
                        "end_line": getattr(node, "end_lineno", node.lineno),
                        "docstring": c_doc,
                        "signature": sig
                    })
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append({"name": alias.name, "alias": alias.asname, "line": node.lineno})
                elif isinstance(node, ast.ImportFrom):
                    mod = node.module or ""
                    for alias in node.names:
                        imports.append({"name": f"{mod}.{alias.name}", "alias": alias.asname, "line": node.lineno})
        except Exception:
            pass

        return {
            "symbols": symbols,
            "imports": imports,
            "docstrings": docstrings
        }

    @staticmethod
    def parse_javascript_typescript(code: str, file_path: str = "") -> Dict[str, Any]:
        symbols = []
        imports = []
        docstrings = []

        lines = code.splitlines()
        for idx, line in enumerate(lines):
            line_num = idx + 1
            l_str = line.strip()

            # Class Regex
            class_match = re.search(r"class\s+([A-Za-z0-9_]+)", l_str)
            if class_match:
                symbols.append({
                    "name": class_match.group(1),
                    "kind": "class",
                    "start_line": line_num,
                    "end_line": line_num,
                    "docstring": None,
                    "signature": l_str
                })

            # Function Regex
            func_match = re.search(r"(?:function|const|let|var)\s+([A-Za-z0-9_]+)\s*=?\s*(?:async\s*)?\((.*?)\)", l_str)
            if func_match and "class" not in l_str:
                symbols.append({
                    "name": func_match.group(1),
                    "kind": "function",
                    "start_line": line_num,
                    "end_line": line_num,
                    "docstring": None,
                    "signature": l_str
                })

            # Import Regex
            import_match = re.search(r"import\s+.*\s+from\s+['"](.*?)['"]", l_str)
            if import_match:
                imports.append({
                    "name": import_match.group(1),
                    "alias": None,
                    "line": line_num
                })

        return {
            "symbols": symbols,
            "imports": imports,
            "docstrings": docstrings
        }

    @classmethod
    def parse_file(cls, content: str, language: str, path: str = "") -> Dict[str, Any]:
        if language == "python":
            return cls.parse_python(content, path)
        elif language in ["typescript", "javascript"]:
            return cls.parse_javascript_typescript(content, path)
        return {"symbols": [], "imports": [], "docstrings": []}
