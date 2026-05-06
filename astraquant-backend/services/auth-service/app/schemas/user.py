from pydantic import BaseModel

class CurrentUserResponse(BaseModel):
    id: str
    username: str
    display_name: str
    roles: list[str]
    permissions: list[str]
