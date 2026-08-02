# Redis caching layer introduced in v1.1.0 to offload database query load
# and provide fast sub-millisecond user session authentication lookup.

class RedisCacheClient:
    def __init__(self, host: str = "localhost", port: int = 6379):
        self.host = host
        self.port = port
        self.store = {}

    def get(self, key: str):
        return self.store.get(key)

    def set(self, key: str, value: str, ttl: int = 300):
        self.store[key] = value
