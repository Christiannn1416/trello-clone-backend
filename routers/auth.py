from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
import models, utils, auth, database

router = APIRouter(tags=['Autenticacion'])

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    #se busca usuario por correo
    user = db.query(models.User).filter(models.User.correo == request.username).first()
    #validaciones
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    if not utils.verify_password(request.password,user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Contraseña incorrecta")
    #generar token si todo es correcto
    access_token = auth.create_access_token(data={"user_id":user.id})
    
    return{"access_token": access_token, "token_type":"bearer"}