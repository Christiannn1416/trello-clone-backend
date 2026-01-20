from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, utils

router = APIRouter(
    prefix = "/usuarios",
    tags = ["Usuarios"]
)

@router.post("/", response_model=schemas.UserResponse)
def crear_usuario(usuario:schemas.UserCreate, db:Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.correo == usuario.correo).first()
    if db_user:
        raise HTTPException(status_code = 400, detail = "El correo ya existe")
    hash_pw =utils.hash_password(usuario.password)
    nuevo_usuario = models.User(
        nombre = usuario.nombre,
        correo = usuario.correo,
        password_hash = hash_pw
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario