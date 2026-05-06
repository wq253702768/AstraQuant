from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    id: str
    username: str
    display_name: str
    status: str
    roles: list[str]
    permissions: list[str]

    @property
    def active(self) -> bool:
        return self.status == "active"
