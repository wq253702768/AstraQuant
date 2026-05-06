SENSITIVE={"api_key","secret_key","passphrase","signature","access_token","refresh_token","password","encrypted_secret_key"}
class AuditRedactionService:
    def redact(self, data):
        if isinstance(data, dict): return {k:("[REDACTED]" if k in SENSITIVE else self.redact(v)) for k,v in data.items()}
        if isinstance(data, list): return [self.redact(v) for v in data]
        return data
