from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/login", refreshUrl="v1/auth/refresh")

TokenDep = Annotated[str, Depends(oauth2_scheme)]

security = HTTPBearer()

CredDep = Annotated[HTTPAuthorizationCredentials, Depends(security)]