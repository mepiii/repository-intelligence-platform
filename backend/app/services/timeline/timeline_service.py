from typing import List, Dict, Any
from datetime import datetime

class TimelineService:
    @staticmethod
    def generate_timeline(commits: List[Dict[str, Any]], dependencies: List[Dict[str, Any]], tags: List[str]) -> List[Dict[str, Any]]:
        events = []

        # 1. Commits and Refactors
        for c in sorted(commits, key=lambda x: x["commit_date"]):
            msg = c["message"]
            is_refactor = "refactor" in msg.lower() or "rewrite" in msg.lower() or "clean" in msg.lower()
            
            events.append({
                "event_type": "refactor" if is_refactor else "commit",
                "description": f"[{c['author_name']}] {msg}",
                "timestamp": c["commit_date"],
                "metadata_json": {"hash": c["hash"], "author": c["author_email"]}
            })

        # 2. Dependency events
        for dep in dependencies:
            events.append({
                "event_type": "dependency_add",
                "description": f"Dependency added: {dep['name']} ({dep.get('version', '*')}) in {dep.get('source_file', 'manifest')}",
                "timestamp": datetime.utcnow(),
                "metadata_json": dep
            })

        # 3. Releases / Tags
        for tag in tags:
            events.append({
                "event_type": "release",
                "description": f"Release tagged: {tag}",
                "timestamp": datetime.utcnow(),
                "metadata_json": {"tag": tag}
            })

        # Sort chronologically
        events.sort(key=lambda x: x["timestamp"], reverse=True)
        return events
