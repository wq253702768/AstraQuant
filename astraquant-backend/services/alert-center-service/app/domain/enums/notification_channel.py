from enum import StrEnum
class NotificationChannel(StrEnum):
    UI_INBOX = "UI_INBOX"
    WEBHOOK = "WEBHOOK"
    EMAIL = "EMAIL"
    FEISHU = "FEISHU"
