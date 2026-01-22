from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from auth import get_current_user

router = APIRouter(
    prefix="/tableros",
    tags=["Tableros"]
)

####################################################TABLEROS####################################################
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

@router.get("/")
def obtener_tableros(db: Session = Depends(get_db)):
    return db.query(models.Board).all()

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
    tableros = db.query(models.Board).filter(models.Board.propietario_id == current_user.id)
    return tableros

###############################################LISTAS###############################################################
#crear lista
@router.post("/listas",response_model=schemas.ListResponse)
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
@router.put("/listas/{list_id}",response_model=schemas.ListResponse)
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
    return None

################################################CARDS##########################################################
#crear card
@router.post("/cards",response_model=schemas.CardResponse)
def crear_card(card: schemas.CardCreate, 
               db: Session = Depends(get_db),
               current_user: models.User = Depends(get_current_user)):
    #obtener un usuario para el creador
    #usuario = db.query(models.User).first()
    #crear el objeto
    nueva_card = models.Card(
        titulo = card.titulo,
        descripcion = card.descripcion,
        posicion = card.posicion,
        fecha_inicio = card.fecha_inicio,
        fecha_vencimiento = card.fecha_vencimiento,
        list_id = card.list_id,
        creado_por = current_user.id
    )
    
    db.add(nueva_card)
    db.commit()
    db.refresh(nueva_card)
    return nueva_card

#borrar card
@router.delete("/cards/{card_id}")
def eliminar_card(
        card_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)):   
    card = db.query(models.Card).filter(
        models.Card.id == card_id,
        models.Card.creado_por == current_user.id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")

    db.delete(card)
    db.commit()
    return{"message:" "Tarjeta eliminada"}

@router.put("/cards/{card_id}")
def actualizar_card(
    card_id: int,
    card_actualizado: schemas.CardUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)):
    #tarjeta que tenga ese ID Y que pertenezca al usuario actual
    query = db.query(models.Card).filter(
        models.Card.id == card_id, 
        models.Card.creado_por == current_user.id
    )
    card_db = query.first()

    if not card_db:
        raise HTTPException(
            status_code=404, 
            detail="Tarjeta no encontrada o no tienes permisos")
    
    #exclude_unset=True evita sobreescribir con nones campos que no se envían
    datos_actualizados = card_actualizado.model_dump(exclude_unset=True)
    query.update(datos_actualizados,
                 synchronize_session=False)
    db.commit()
    db.refresh(card_db)
    return card_db
