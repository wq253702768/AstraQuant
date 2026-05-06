import hashlib
import json

class InputDataHashService:
    def calculate(self, input_data: dict) -> str:
        normalized = json.dumps(input_data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
