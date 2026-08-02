class DatabaseConnection:
    def __init__(self, uri: str = "sqlite:///sample.db"):
        self.uri = uri

    def connect(self):
        return f"Connected to {self.uri}"
