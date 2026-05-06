from pydantic import BaseModel, Field

class PageQuery(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=200)
    cursor: str | None = None

class PageResult(BaseModel):
    items: list[object]
    total: int | None = None
    page: int | None = None
    page_size: int | None = None
    next_cursor: str | None = None
