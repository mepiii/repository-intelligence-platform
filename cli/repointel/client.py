import requests

class RepointelClient:
    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        self.base_url = base_url

    def scan(self, path: str):
        repo_resp = requests.post(f"{self.base_url}/repositories", json={"name": "local-repo", "path": path})
        repo_data = repo_resp.json()
        repo_id = repo_data["id"]
        scan_resp = requests.post(f"{self.base_url}/repositories/{repo_id}/scan")
        return scan_resp.json()

    def index(self, repo_id: int = 1):
        return requests.post(f"{self.base_url}/repositories/{repo_id}/index").json()

    def search(self, query: str, repo_id: int = 1):
        return requests.get(f"{self.base_url}/search", params={"repo_id": repo_id, "q": query}).json()

    def get_graph(self, repo_id: int = 1):
        return requests.get(f"{self.base_url}/graph", params={"repo_id": repo_id}).json()

    def get_timeline(self, repo_id: int = 1):
        return requests.get(f"{self.base_url}/timeline", params={"repo_id": repo_id}).json()

    def get_debt(self, repo_id: int = 1):
        return requests.get(f"{self.base_url}/technical-debt", params={"repo_id": repo_id}).json()

    def ask(self, prompt: str, repo_id: int = 1):
        return requests.post(f"{self.base_url}/assistant/chat", json={"repo_id": repo_id, "message": prompt}).json()
