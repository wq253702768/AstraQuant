from dataclasses import asdict


class LifecycleTimelineBuilder:
    def build(self, events: list, strategy_version_id: str) -> list[dict]:
        items = []
        for event in events:
            if event.strategy_version_id == strategy_version_id:
                data = asdict(event)
                data["item_type"] = "EVENT"
                items.append(data)
        return sorted(items, key=lambda item: str(item.get("occurred_at") or ""))
