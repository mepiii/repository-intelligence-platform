import networkx as nx
from typing import Dict, Any, List
from app.core.config import settings

class GraphService:
    def __init__(self):
        self.nx_graph = nx.DiGraph()
        self.neo4j_driver = None
        self._init_neo4j()

    def _init_neo4j(self):
        try:
            from neo4j import GraphDatabase
            self.neo4j_driver = GraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
            )
        except Exception:
            self.neo4j_driver = None

    def build_graph_from_repo_data(self, repo_id: int, repo_name: str, files: List[Dict[str, Any]], commits: List[Dict[str, Any]], symbols_map: Dict[str, Any]):
        self.nx_graph.clear()
        
        # Repository Node
        repo_node_id = f"repo:{repo_id}"
        self.nx_graph.add_node(repo_node_id, label="Repository", name=repo_name, type="repository")

        # Developer & Commit Nodes
        for c in commits:
            commit_id = f"commit:{c['hash'][:8]}"
            dev_id = f"dev:{c['author_email']}"

            self.nx_graph.add_node(commit_id, label="Commit", name=c['hash'][:8], type="commit", message=c['message'])
            self.nx_graph.add_node(dev_id, label="Developer", name=c['author_name'], type="developer", email=c['author_email'])
            
            self.nx_graph.add_edge(dev_id, commit_id, label="AUTHORED_BY")
            self.nx_graph.add_edge(repo_node_id, commit_id, label="CONTAINS")

        # File & Symbol Nodes
        for f in files:
            path = f["path"]
            file_id = f"file:{path}"
            self.nx_graph.add_node(file_id, label="File", name=path, type="file", language=f["language"])
            self.nx_graph.add_edge(repo_node_id, file_id, label="CONTAINS")

            symbols = symbols_map.get(path, [])
            for sym in symbols:
                sym_id = f"sym:{path}:{sym['name']}"
                kind = sym["kind"]
                sym_label = "Class" if kind == "class" else "Function"
                
                self.nx_graph.add_node(sym_id, label=sym_label, name=sym['name'], type=kind.lower())
                self.nx_graph.add_edge(file_id, sym_id, label="DEFINES")

        # Sync to Neo4j if available
        self._sync_to_neo4j()

    def _sync_to_neo4j(self):
        if not self.neo4j_driver:
            return
        try:
            with self.neo4j_driver.session() as session:
                for node, attrs in self.nx_graph.nodes(data=True):
                    label = attrs.get("label", "Node")
                    session.run(
                        f"MERGE (n:{label} {{id: $id}}) SET n += $props",
                        id=node,
                        props=attrs
                    )
                for u, v, attrs in self.nx_graph.edges(data=True):
                    rel = attrs.get("label", "RELATED_TO")
                    session.run(
                        f"MATCH (a {{id: $u}}), (b {{id: $v}}) MERGE (a)-[r:{rel}]->(b)",
                        u=u, v=v
                    )
        except Exception as e:
            print(f"Neo4j sync note: {e}")

    def get_graph_data(self) -> Dict[str, Any]:
        nodes = []
        for n, attrs in self.nx_graph.nodes(data=True):
            nodes.append({
                "id": str(n),
                "label": attrs.get("label", "Node"),
                "name": attrs.get("name", str(n)),
                "type": attrs.get("type", "unknown"),
                "properties": attrs
            })

        edges = []
        for idx, (u, v, attrs) in enumerate(self.nx_graph.edges(data=True)):
            edges.append({
                "id": f"e_{idx}",
                "source": str(u),
                "target": str(v),
                "label": attrs.get("label", "RELATED")
            })

        return {"nodes": nodes, "edges": edges}

    def close(self):
        if self.neo4j_driver:
            self.neo4j_driver.close()

graph_service = GraphService()
