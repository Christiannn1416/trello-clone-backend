from database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, index = True)
    nombre = Column(String, nullable = False)
    correo = Column(String, unique = False, index = True, nullable = False)
    password_hash = Column(String, nullable = False)
    fecha_creacion = Column(DateTime, default = datetime.utcnow)
    #relacion con los tableros creados
    tableros = relationship("Board", back_populates = "propietario")
    #relacion con las cards creados
    cards_creadas = relationship("Card", back_populates = "creador")
    
class Board(Base):
    __tablename__ = "boards"
    id = Column(Integer, primary_key = True, index = True)
    titulo = Column(String, nullable = False)
    propietario_id = Column(Integer, ForeignKey("users.id")) #relación con el usuario propietario
    fecha_creacion = Column(DateTime, default = datetime.utcnow)
    
    #permite acceder al dueño desde el objeto tablero
    propietario = relationship("User", back_populates = "tableros")
    #relación a listas
    listas = relationship("List",back_populates="board", cascade="all, delete_orphan")
    
#listas de cada tablero
class List(Base):
    __tablename__ = "lists"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable = False)
    orden = Column(Integer, default = 0)
    board_id = Column(Integer, ForeignKey("boards.id"), ondelete="CASCADE")
    #relacion una ista pertenece a un tablero
    board = relationship("Board", back_populates="listas")
    #relacion con las cards
    cards = relationship("Card", back_populates = "lista", cascade="all, delete_orphan")
    
class Card(Base):
    __tablename__ = "cards"
    id = Column (Integer, primary_key=True, index=True)
    titulo = Column(String, nullable = False)
    descripcion = Column(String, nullable = True)
    posicion = Column(Integer, default = 0)
    fecha_inicio = Column(DateTime)
    fecha_vencimiento = Column(DateTime)
    list_id = Column(Integer,ForeignKey("lists.id"), ondelete="CASCADE")
    creado_por = Column(Integer, ForeignKey("users.id"))
    #relacion con la lista donde se encuentra
    lista = relationship("List", back_populates = "cards")
    #relacion qn la creó
    creador = relationship("User", back_populates = "cards_creadas")