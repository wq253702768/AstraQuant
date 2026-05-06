from app.domain.services.report_filename_builder import ReportFilenameBuilder
from app.domain.services.report_payload_builder import ReportPayloadBuilder
from app.infrastructure.minio.minio_client import MinIOClient
from app.renderers.html_renderer import HTMLRenderer
from app.renderers.json_renderer import JSONRenderer


def test_build_backtest_report_payload():
    payload = ReportPayloadBuilder().build("BACKTEST_REPORT", "bt_001")
    assert payload["report_type"] == "BACKTEST_REPORT"


def test_build_drawdown_report_payload():
    payload = ReportPayloadBuilder().build("DRAWDOWN_REPORT", "dd_001")
    assert payload["related_id"] == "dd_001"


def test_build_ai_report_payload():
    assert ReportPayloadBuilder().build("AI_ANALYSIS_REPORT", "ai_001")["report_type"] == "AI_ANALYSIS_REPORT"


def test_html_renderer():
    html = HTMLRenderer().render("BACKTEST_REPORT", {"report_type": "BACKTEST_REPORT", "summary": "ok", "sections": ["A"]})
    assert "BACKTEST_REPORT" in html


def test_json_renderer():
    content = JSONRenderer().render({"a": 1})
    assert '"a": 1' in content


def test_report_filename_builder():
    builder = ReportFilenameBuilder()
    assert builder.bucket("BACKTEST_REPORT") == "backtest-reports"
    assert builder.object_key("BACKTEST_REPORT", "bt_001", "HTML").endswith("bt_001.html")


def test_minio_upload_mock():
    result = MinIOClient().upload_text("bucket", "a.txt", "hello", "text/plain")
    assert result["file_size"] == 5
