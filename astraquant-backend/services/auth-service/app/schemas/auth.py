from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1)

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class LogoutRequest(BaseModel):
    refresh_token: str

class ChangePasswordRequest(BaseModel):
    old_password: str = Field(min_length=1)
    new_password: str = Field(min_length=8)

class UserTokenInfo(BaseModel):
    id: str
    username: str
    display_name: str
    roles: list[str]

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    user: UserTokenInfo

class RefreshTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int

class OperationSuccessResponse(BaseModel):
    success: bool
