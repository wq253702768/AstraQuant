from datetime import UTC, datetime
BUCKETS = {"BACKTEST_REPORT": "backtest-reports", "DRAWDOWN_REPORT": "drawdown-reports", "AI_ANALYSIS_REPORT": "ai-reports", "STRATEGY_SCORE_REPORT": "strategy-score-reports"}
class ReportFilenameBuilder:
    def bucket(self, report_type: str) -> str: return BUCKETS[report_type]
    def object_key(self, report_type: str, related_id: str, file_format: str) -> str:
        now = datetime.now(UTC)
        return f"{now.year}/{now.month:02d}/{related_id}.{file_format.lower()}"
