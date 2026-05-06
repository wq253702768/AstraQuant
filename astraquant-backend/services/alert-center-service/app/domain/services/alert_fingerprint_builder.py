import hashlib, json
class AlertFingerprintBuilder:
    def build(self, event: dict) -> str:
        fields = event.get("fingerprint_fields") or {k: event.get(k) for k in ["source","rule_code","account_id","strategy_version_id","internal_symbol","resource_type"]}
        raw = json.dumps(fields, sort_keys=True, ensure_ascii=False, default=str)
        return hashlib.sha256(raw.encode()).hexdigest()
