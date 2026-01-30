from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
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

#cards
class CardBase(BaseModel):
    titulo: str
    descripcion : Optional[str] = None
    posicion: Optional[int] = 0
    fecha_inicio: Optional[datetime] = None
    fecha_vencimiento: Optional[datetime] = None
class CardCreate(CardBase):
    list_id: int
class CardResponse(BaseModel):
    id: int
    titulo: str
    descripcion: Optional[str]
    posicion: int
    list_id: int
    fecha_inicio: Optional[datetime] = None
    fecha_vencimiento: Optional[datetime] = None
    class Config:
        from_attributes = True
class CardUpdate(BaseModel):
    titulo: Optional[str]
    descripcion : Optional[str] = None
    posicion: Optional[int] = 0
    fecha_inicio: Optional[datetime] = None
    fecha_vencimiento: Optional[datetime] = None
    list_id: Optional[int] = None
#card con todo su contenido response
class CardInList(CardResponse):
    pass

#listas
class ListBase(BaseModel):
    titulo: str
    orden: Optional[int] = 0
class ListCreate(ListBase):
    board_id: int #siempre se necesita saber el tablero al que se dirige
class ListResponse(BaseModel):
    id: int
    titulo: str
    orden: int
    cards: List[CardResponse] = [] #cards que tiene la lista
    class Config:
        from_attributes = True
class ListUpdate(BaseModel):
    titulo: Optional[str] = None
    orden: Optional[int] = None
        
#lista con sus cards
class ListWithCards(ListResponse):
    cards: list[CardInList] = []
    
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
#tablero con sus listas
class BoardFullResponse(BaseModel):
    id: int
    titulo: str
    listas: list[ListResponse] = []
    class Config:
        from_attributes =  True
