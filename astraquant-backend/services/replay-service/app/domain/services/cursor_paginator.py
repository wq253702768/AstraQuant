import base64

class CursorPaginator:
    def encode(self, offset: int) -> str:
        return base64.urlsafe_b64encode(str(offset).encode()).decode()
    def decode(self, cursor: str | None) -> int:
        if not cursor:
            return 0
        return int(base64.urlsafe_b64decode(cursor.encode()).decode())
    def page(self, items: list, limit: int, cursor: str | None = None) -> tuple[list, str | None]:
        offset = self.decode(cursor)
        page = items[offset:offset + limit]
        next_offset = offset + len(page)
        return page, self.encode(next_offset) if next_offset < len(items) else None
