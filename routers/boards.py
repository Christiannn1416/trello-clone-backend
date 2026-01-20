from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(
    prefix="/tableros",
    tags=["Tableros"]
)

@router.post("/",response_model=schemas.BoardResponse)
def crear_tablero(tablero:schemas.BoardCreate, db: Session = Depends(get_db)):
    #se busca al primer usuario de la base para asignarlo al tablero
    usuario = db.query(models.User).first()
    
    if not usuario:
        raise HTTPException(status_code = 404, detail="No hay usuarios registrados")
    nuevo_tablero = models.Board(
        titulo = tablero.titulo,
        propietario_id = usuario.id
    )
    
    db.add(nuevo_tablero)
    db.commit()
    db.refresh(nuevo_tablero)
    return nuevo_tablero

@router.get("/")
def obtener_tableros(db: Session = Depends(get_db)):
    return db.query(models.Board).all()

@router.post("/listas",response_model=schemas.ListResponse)
def crear_lista(lista: schemas.ListCreate, db: Session = Depends(get_db)):
    #verificar si el tablero existe
    tablero = db.query(models.Board).filter(models.Board.id == lista.board_id).first()
    if not tablero:
        raise HTTPException(status_code=404, detail="Tablero no encontrado")
    nueva_lista = models.List(
        titulo = lista.titulo,
        orden = lista.orden,
        board_id = lista.board_id
    )

    db.add(nueva_lista)
    db.commit()
    db.refresh(nueva_lista)
    return nueva_lista

@router.post("/cards",response_model=schemas.CardResponse)
def crear_card(card: schemas.CardCreate, db: Session = Depends(get_db)):
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
        creado_por = card.creado_por
    )
    
    db.add(nueva_card)
    db.commit()
    db.refresh(nueva_card)
    return nueva_card

#tablero con toda su info
@router.get("/{board_id}",response_model=schemas.BoardFullResponse)
def obtener_detalle_tablero(board_id: int, db: Session = Depends(get_db)):
    tablero = db.query(models.Board).filter(models.Board.id == board_id).first()
    if not tablero:
        raise HTTPException(status_code=404, detail="Tablero no encontrado")
    return tablero