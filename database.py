import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Carga las variables del archivo .env a las variables de entorno del sistema
# 1. CARGAR primero
load_dotenv() 

# 2. OBTENER después
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# 3. VERIFICAR (esto te ayudará a debuguear)
if SQLALCHEMY_DATABASE_URL is None:
    raise ValueError("ERROR: La variable DATABASE_URL no se encontró en el archivo .env")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()