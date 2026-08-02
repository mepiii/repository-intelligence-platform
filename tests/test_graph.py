from app.services.graph.neo4j_service import GraphService

def test_graph_building():
    svc = GraphService()
    files = [{"path": "main.py", "language": "python"}]
    commits = [{"hash": "abc12345", "author_name": "Dev", "author_email": "dev@example.com", "message": "initial commit"}]
    symbols = {"main.py": [{"name": "main", "kind": "function"}]}
    
    svc.build_graph_from_repo_data(1, "Sample", files, commits, symbols)
    data = svc.get_graph_data()
    assert len(data["nodes"]) >= 4
    assert len(data["edges"]) >= 3
