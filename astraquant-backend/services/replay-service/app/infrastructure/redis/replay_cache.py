class ReplayCache:
    def __init__(self): self.memory = {}
    async def get(self, key: str): return self.memory.get(key)
    async def set(self, key: str, value, ttl_seconds: int): self.memory[key] = value
