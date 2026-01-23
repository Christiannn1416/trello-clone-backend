from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from auth import get_current_user

router = APIRouter(
    prefix="/cards",
    tags=["Cards"]
)

#crear card
@router.post("/",response_model=schemas.CardResponse)
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
@router.delete("/{card_id}")
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

@router.put("/{card_id}")
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
