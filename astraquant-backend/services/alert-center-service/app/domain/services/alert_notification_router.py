class AlertNotificationRouter:
    def channels(self, level: str) -> list[str]:
        return {"INFO":["UI_INBOX"],"WARNING":["UI_INBOX","EMAIL"],"CRITICAL":["UI_INBOX","EMAIL","WEBHOOK"],"FATAL":["UI_INBOX","EMAIL","WEBHOOK","FEISHU"]}.get(level,["UI_INBOX"])
