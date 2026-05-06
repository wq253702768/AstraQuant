class DataLoader:
    def load(self, rows: list[dict]) -> list[dict]:
        return sorted(rows, key=lambda item: item["ts"])
