import jwt
from datetime import datetime , timezone , timedelta
from pwdlib import PasswordHash
from config import setting  
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

PasswordHashContext = PasswordHash.recommended()

def hash_passward(passward:str)->str:
    return PasswordHashContext.hash(password=passward)

def varify_passward(passward:str,hash_passward:str)->bool:
    return PasswordHashContext.verify(passward,hash_passward)

def generate_token(data:dict)->str:
    encode = data.copy()
    expiry = datetime.now(timezone.utc) + timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    encode.update({'exp':expiry})
    jwt_token = jwt.encode(encode,setting.JWT_SECRET_KEY,algorithm=setting.JWT_ALGORITHM)
    return jwt_token

def get_current_user_email(token:Annotated[str,Depends(oauth2_scheme)])->str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials/Token expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decode = jwt.decode(token,setting.JWT_SECRET_KEY, algorithms=[setting.JWT_ALGORITHM])
        email:str = decode.get('sub')
        if email is None:
            raise credentials_exception
        return email
    except jwt.exceptions:
        raise credentials_exception
    
