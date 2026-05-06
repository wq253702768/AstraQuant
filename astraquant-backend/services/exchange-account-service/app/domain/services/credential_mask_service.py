class CredentialMaskService:
    def mask(self, api_key: str) -> str:
        if len(api_key) <= 8: return api_key[:2] + "****" + api_key[-2:]
        return api_key[:4] + "****" + api_key[-4:]
