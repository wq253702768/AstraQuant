class HandleRiskCheckedService:
    async def handle(self, event: dict):
        if event.get("decision") not in {"APPROVE", "REDUCE_ONLY"}: return None
        return {"status": "ACCEPTED"}
