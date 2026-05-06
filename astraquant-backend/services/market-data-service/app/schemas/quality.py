from pydantic import BaseModel

class QualityReportResponse(BaseModel):
    status: str
    expected_count: int | None = None
    actual_count: int | None = None
    missing_count: int | None = None
    duplicate_count: int | None = None
    abnormal_count: int | None = None
    missing_ranges: list | None = None
    warning_items: list | None = None
