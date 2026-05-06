class ScoreExplanationBuilder:
    def build(self, scores: dict, warnings: list[str], suggestions: list[dict]) -> dict:
        return {"scores": scores, "warnings": warnings, "suggestions": suggestions}
