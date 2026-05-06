class AlertDedupService:
    def __init__(self): self.seen = {}
    def hit(self, fingerprint: str) -> bool:
        if fingerprint in self.seen:
            self.seen[fingerprint] += 1; return True
        self.seen[fingerprint] = 1; return False
