from passlib.context import CryptContext
# 1. configuración de algoritmo de encriptación (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

#convierte texto en un hash seguro
def hash_password(password: str):
    return pwd_context.hash(password)

#compara una clave escrita con el hash guardado en la base de datos
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)