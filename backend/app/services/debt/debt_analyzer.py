import re
from typing import List, Dict, Any

class DebtAnalyzer:
    @staticmethod
    def analyze_file(file_path: str, content: str, symbols: List[Dict[str, Any]]) -> Dict[str, Any]:
        issues = []
        lines = content.splitlines()
        line_count = len(lines)

        # 1. Long File Check
        if line_count > 300:
            issues.append({
                "rule": "LONG_FILE",
                "message": f"File contains {line_count} lines (exceeds threshold of 300).",
                "severity": "medium",
                "line": None
            })

        # 2. Long Functions & Large Classes
        for sym in symbols:
            start = sym.get("start_line", 0)
            end = sym.get("end_line", start)
            length = end - start + 1

            if sym["kind"] == "function" and length > 50:
                issues.append({
                    "rule": "LONG_FUNCTION",
                    "message": f"Function '{sym['name']}' has {length} lines (exceeds 50).",
                    "severity": "medium",
                    "line": start
                })
            elif sym["kind"] == "class" and length > 150:
                issues.append({
                    "rule": "LARGE_CLASS",
                    "message": f"Class '{sym['name']}' has {length} lines (exceeds 150).",
                    "severity": "medium",
                    "line": start
                })

        # 3. TODO accumulation
        todo_count = 0
        for idx, line in enumerate(lines):
            if "TODO" in line or "FIXME" in line or "HACK" in line:
                todo_count += 1
                issues.append({
                    "rule": "TODO_FOUND",
                    "message": f"Technical debt marker found: {line.strip()}",
                    "severity": "low",
                    "line": idx + 1
                })

        # 4. Missing Tests Check (heuristic)
        if not ("test" in file_path.lower() or "spec" in file_path.lower()) and file_path.endswith((".py", ".ts", ".js")):
            if "def " in content or "function " in content:
                issues.append({
                    "rule": "MISSING_TEST_COVERAGE",
                    "message": "Source module has no direct test counterpart detected.",
                    "severity": "low",
                    "line": 1
                })

        # Calculate file-level debt score
        raw_penalty = sum(15 if i["severity"] == "high" else 10 if i["severity"] == "medium" else 5 for i in issues)
        debt_score = min(100.0, float(raw_penalty))
        maintainability_score = max(0.0, round(100.0 - debt_score, 1))

        suggestions = []
        if any(i["rule"] == "LONG_FILE" for i in issues):
            suggestions.append(f"Consider splitting {file_path} into smaller, modular files.")
        if any(i["rule"] == "LONG_FUNCTION" for i in issues):
            suggestions.append("Refactor long functions into smaller helper functions.")
        if todo_count > 0:
            suggestions.append(f"Resolve {todo_count} pending TODO/FIXME comments.")

        return {
            "file_path": file_path,
            "line_count": line_count,
            "debt_score": debt_score,
            "maintainability_score": maintainability_score,
            "issues": issues,
            "suggestions": suggestions
        }

    @classmethod
    def analyze_repository(cls, files: List[Dict[str, Any]], symbols_map: Dict[str, Any]) -> Dict[str, Any]:
        file_reports = []
        total_debt = 0.0
        total_maint = 0.0

        for f in files:
            path = f["path"]
            content = f.get("content", "")
            syms = symbols_map.get(path, [])
            report = cls.analyze_file(path, content, syms)
            file_reports.append(report)
            total_debt += report["debt_score"]
            total_maint += report["maintainability_score"]

        count = len(files) if files else 1
        overall_debt = round(total_debt / count, 1)
        overall_maint = round(total_maint / count, 1)

        all_suggestions = []
        for r in file_reports:
            all_suggestions.extend(r["suggestions"])

        return {
            "overall_debt_score": overall_debt,
            "overall_maintainability_score": overall_maint,
            "file_reports": file_reports,
            "suggestions": list(set(all_suggestions))
        }
