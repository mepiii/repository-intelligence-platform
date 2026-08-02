from app.services.intelligence.ast_parser import ASTParser
from typing import List, Dict, Any

class SymbolIndexer:
    def __init__(self):
        self.symbol_index = {}
        self.reference_index = {}
        self.import_graph = {}

    def index_files(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        for f in files:
            path = f["path"]
            lang = f["language"]
            content = f.get("content", "")

            parsed = ASTParser.parse_file(content, lang, path)
            self.symbol_index[path] = parsed["symbols"]
            self.import_graph[path] = [imp["name"] for imp in parsed["imports"]]

        return {
            "symbol_index": self.symbol_index,
            "import_graph": self.import_graph
        }
