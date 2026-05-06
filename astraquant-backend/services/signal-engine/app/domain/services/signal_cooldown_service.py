import time
class SignalCooldownService:
    def __init__(self): self.expires={}
    def allow(self, key: str, seconds: int) -> bool:
        now=time.time()
        if self.expires.get(key, 0) > now: return False
        self.expires[key]=now+seconds
        return True
