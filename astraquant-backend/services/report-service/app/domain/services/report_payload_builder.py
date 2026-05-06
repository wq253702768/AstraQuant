class ReportPayloadBuilder:
    def build(self, report_type: str, related_id: str) -> dict:
        return {"report_type": report_type, "related_id": related_id, "summary": "AstraQuant 报告基础版", "sections": ["摘要", "风险提示", "后续建议"]}
