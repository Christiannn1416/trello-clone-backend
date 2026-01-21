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
@router.put("/{list_id}",response_model=schemas.ListResponse)
def actualizar_lista(
    list_id: int,
    lista_update: schemas.ListCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)    
):
    #verificar propiedad a través del tablero
    lista_db = db.query(models.List).join(models.Board).filter(
        models.List.id == list_id,
        models.Board.propietario_id == current_user.id
    ).first()
    if not lista_db:
        raise HTTPException(status_code=404, detail="Lista no encontrada")
    
    lista_db.nombre = lista_update.titulo
    lista_db.orden = lista_update.orden
    
    db.commit()
    db.refresh(lista_db)
    return lista_db

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
def crear_card(card: schemas.CardCreate, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
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

#update card
@router.put("/{card_id}",response_model=schemas.CardResponse)
def actualizar_card(
    card_id: int,
    card_update: schemas.CardUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    #verificar que la tarjeta pertenezca a un tablero del usuario
    tarjeta_db: db.query(models.Card).join(models.List).join(models.Board).filter(
        models.Card.id == card_id,
        models.Board.propietario_id == current_user.id
    ).first()