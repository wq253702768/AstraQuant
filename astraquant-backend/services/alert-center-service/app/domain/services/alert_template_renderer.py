class AlertTemplateRenderer:
    def render(self, event: dict) -> str: return event.get("message", "")
