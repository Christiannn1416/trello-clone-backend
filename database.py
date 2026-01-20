from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABSE_URL = "postgresql://trelloclonedb_user:ckF6txsRI51SYENJWXu5HqhecTC4xoDq@dpg-d5nc43ur433s739m09k0-a.ohio-postgres.render.com/trelloclonedb?sslmode=require"

engine = create_engine(SQLALCHEMY_DATABSE_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()