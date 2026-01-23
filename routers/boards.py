from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from auth import get_current_user

router = APIRouter(
    prefix="/tableros",
    tags=["Tableros"]
)
#crear tablero
@router.post("/",response_model=schemas.BoardResponse)
def crear_tablero(tablero:schemas.BoardCreate, 
                  db: Session = Depends(get_db),
                  current_user: models.User = Depends(get_current_user)):
    
    nuevo_tablero = models.Board(
        titulo = tablero.titulo,
        propietario_id = current_user.id
    )
    
    db.add(nuevo_tablero)
    db.commit()
    db.refresh(nuevo_tablero)
    return nuevo_tablero

#update tablero
@router.put("/{board_id}",response_model=schemas.BoardResponse)
def actualizar_tablero(
  board_id: int,
  tablero_actualizado: schemas.BoardCreate,
  db: Session = Depends(get_db),
  current_user: models.User = Depends(get_current_user)  
):
    #buscar tablero y verificar propiedar
    query = db.query(models.Board).filter(
        models.Board.id == board_id, 
        models.Board.propietario_id == current_user.id
    )
    tablero_db = query.first()
    if not tablero_db:
        raise HTTPException(status_code=404, detail="Tablero no encontrado")
    #actualizar cambios
    query.update(tablero_actualizado.dict(),synchronize_session=False)
    
    db.commit()
    db.refresh(tablero_db)
    return tablero_db

#borrar tablero
@router.delete("/{board_id}",status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tablero(
  board_id: int,
  db: Session = Depends(get_db),
  current_user: models.User = Depends(get_current_user)  
):
    tablero = db.query(models.Board).filter(
        models.Board.id == board_id,
        models.Board.propietario_id == current_user.id
    ).first()
    if not tablero:
        raise HTTPException(status_code=404, detail="Tablero no encontrado")
    
    db.delete(tablero)
    db.commit()
    return None

#tablero con toda su info
@router.get("/{board_id}",response_model=schemas.BoardFullResponse)
def obtener_detalle_tablero(board_id: int, 
                            db: Session = Depends(get_db),
                            current_user: models.User = Depends(get_current_user)
                            ):
    tablero = db.query(models.Board).filter(
        models.Board.id == board_id,
        models.Board.propietario_id == current_user.id
    ).first()
    if not tablero:
        raise HTTPException(status_code=404, detail="Tablero no encotrado")
    return tablero

#mis tableros
@router.get("/",response_model=list[schemas.BoardResponse])
def listar_mis_tableros(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)):
    #se trae los tableros del usuario loggeado
    tableros = db.query(models.Board).filter(models.Board.propietario_id == current_user.id).all()
    return tableros

