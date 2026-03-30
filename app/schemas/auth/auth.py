from ..default import *

class AuthSchemaPostRequest(BaseModel):
    name: str
    password: str


class AuthSchemaPostResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RegisterSchemaPostRequest(BaseModel):
    name: str
    password: str


class RegisterSchemaPostResponse(BaseModel):
    access_token: str
    refresh_token: str