class AIScore:
    def calculate(self, ai_result: dict | None) -> tuple[float, list[str]]:
        if not ai_result: return 50, ["未执行 AI 审查"]
        risk = str(ai_result.get("risk_level") or ai_result.get("summary", {}).get("risk_level", "MEDIUM"))
        rec = str(ai_result.get("final_recommendation") or ai_result.get("summary", {}).get("final_recommendation", ""))
        if risk == "CRITICAL": return 0, []
        if risk == "HIGH": return 30, []
        if risk == "MEDIUM" or rec == "RETEST_REQUIRED": return 60, []
        if risk == "LOW": return 80, []
        return 50, []
