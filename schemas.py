from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

#lo que se pide para crear un usuario
class UserCreate(BaseModel):
    nombre: str
    correo: EmailStr #valida que el email sea real
    password: str = Field(..., min_length = 8, max_length = 72)

#lo que devuelve al consultar un usuario (sin password)
class UserResponse(BaseModel):
    id: int
    nombre: str
    correo: str
    fecha_creacion: datetime
    class Config:
        from_attributes = True

#tableros
class BoardBase(BaseModel):
    titulo: str
class BoardCreate(BoardBase):
    pass #sólo pide nombre y descripción al crear
class BoardResponse(BoardBase):
    id: int
    propietario_id: int
    fecha_creacion: datetime
    class Config:
        from_attributes =  True
#listas
class ListBase(BaseModel):
    titulo: str
    orden: Optional[int] = 0
class ListCreate(ListBase):
    board_id: int #siempre se necesita saber el tablero al que se dirige
class ListResponse(ListBase):
    id: int
    board_id: int
    
    class Config:
        from_attributes = True
        
#cards
class CardBase(BaseModel):
    titulo: str
    descripcion : Optional[str] = None
    posicion: Optional[int] = 0
    fecha_inicio: Optional[datetime] = None
    fecha_vencimiento: Optional[datetime] = None
class CardCreate(CardBase):
    list_id: int
    creado_por: int
class CardResponse(CardBase):
    id: int
    list_id: int
    creado_por: int
    class Config:
        from_attributes = True
class CardUpdate(BaseModel):
    titulo: Optional[str]
    descripcion : Optional[str] = None
    posicion: Optional[int] = 0
    fecha_inicio: Optional[datetime] = None
    fecha_vencimiento: Optional[datetime] = None
    list_id: Optional[int]
        
#card con todo su contenido response
class CardInList(CardResponse):
    pass 
#lista con sus cards
class ListWithCards(ListResponse):
    cards: list[CardInList] = []
#tablero con sus listas
class BoardFullResponse(BoardResponse):
    listas: list[ListWithCards] = []