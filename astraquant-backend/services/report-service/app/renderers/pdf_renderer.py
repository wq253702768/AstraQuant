class PDFRenderer:
    def render(self, html: str) -> bytes:
        return html.encode("utf-8")
