from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import models, database

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440 #TOKEN QUE DURA 24 HORAS

#crea una cadena de texto encriptada (JWT) con los datos del usuario
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Token de acceso invalido",
        headers = {"WWW-Authenticate:" "Bearer"},
    )
    try:
        #abre token
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id : int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    #busca si el user del token existe en la BD
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    return user
