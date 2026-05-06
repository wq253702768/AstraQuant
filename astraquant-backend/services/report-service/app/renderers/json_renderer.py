import json
class JSONRenderer:
    def render(self, payload: dict) -> str:
        return json.dumps(payload, ensure_ascii=False, default=str, indent=2)
