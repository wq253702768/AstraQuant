from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

class HTMLRenderer:
    def __init__(self):
        template_dir = Path(__file__).resolve().parents[1] / "templates"
        self.env = Environment(loader=FileSystemLoader(template_dir), autoescape=select_autoescape(["html"]))
    def render(self, report_type: str, payload: dict) -> str:
        template = self.env.get_template(self._template(report_type))
        return template.render(payload=payload)
    def _template(self, report_type: str) -> str:
        return {"BACKTEST_REPORT": "backtest_report.html", "DRAWDOWN_REPORT": "drawdown_report.html", "AI_ANALYSIS_REPORT": "ai_report.html", "STRATEGY_SCORE_REPORT": "strategy_score_report.html"}.get(report_type, "base.html")
