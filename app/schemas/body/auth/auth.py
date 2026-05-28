from ..default import *

class LoginSchemaPostRequest(BaseModel):
    username: str
    password: str


class LoginSchemaPostResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class RegisterSchemaPostRequest(BaseModel):
    username: str
    password: str


class RegisterSchemaPostResponse(BaseModel):
    access_token: str
    refresh_token: str