from datetime import datetime, timedelta, UTC

from jose import jwt, JWTError
from passlib.context import CryptContext

import config


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(user: str) -> str:
    expire = datetime.now(UTC) + timedelta(
        minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": user}
    encoded_jwt = jwt.encode(to_encode, 
                             config.SECRET_KEY, 
                             algorithm=config.ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, 
                             config.SECRET_KEY, 
                             algorithms=[config.ALGORITHM])
        return payload["sub"]
    except JWTError:
        return None

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

