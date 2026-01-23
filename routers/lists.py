from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from auth import get_current_user

router = APIRouter(
    prefix="/listas",
    tags=["Listas"]
)

#crear lista
@router.post("/",response_model=schemas.ListResponse)
def crear_lista(lista: schemas.ListCreate,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)
                ):
    #se verifica que el tablero exista y pertenezca al usuario
    tablero = db.query(models.Board).filter(
        models.Board.id == lista.board_id,
        models.Board.propietario_id == current_user.id
    ).first()
    if not tablero:
        raise HTTPException(status_code=403, detail="No puedes crear listas en este tablero")
    
    nueva_lista = models.List(
        titulo = lista.titulo,
        orden = lista.orden,
        board_id = lista.board_id
    )
    db.add(nueva_lista)
    db.commit()
    db.refresh(nueva_lista)
    return nueva_lista

#update lista
@router.put("/{list_id}",response_model=schemas.ListResponse)
def actualizar_lista(
    list_id: int,
    lista_update: schemas.ListUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)    
):
    #lista que tenga el id y que el usuario sea dueño del tablero
    query = db.query(models.List).filter(
        models.List.id == list_id)
    list_db = query.first()
    
    if not list_db:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada o no tienes permisos")
    
    datos_actualziados = lista_update.model_dump(exclude_unset=True)
    query.update(datos_actualziados,synchronize_session=False)
    db.commit()
    db.refresh(list_db)
    return list_db

#eliminar lista
@router.delete("/{list_id}")
def eliminar_lista(
    list_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    lista = db.query(models.List).join(models.Board).filter(
        models.List.id == list_id,
        models.Board.propietario_id == current_user.id
    ).first()
    if not lista:
        raise HTTPException(status_code=404, detail="Lista no encontrada")
    
    db.delete(lista)
    db.commit()
    return {"message": "Borrado exitoso"}