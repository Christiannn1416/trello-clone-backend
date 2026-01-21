from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from routers import users, boards, auth

app = FastAPI(title="Trello Clone API")

origins = [
    "http://localhost",
    "http://localhost:3000", # Puerto común de React
    "http://localhost:5173", # Puerto común de Vite/Vue
    "https://tu-frontend.vercel.app", # Cuando subas tu frontend, agrégalo aquí
    "*", # EL COMODÍN: Permite cualquier origen (útil para pruebas, pero úsalo con cuidado)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Por ahora ponemos "*" para que no tengas problemas al probar
    allow_credentials=True,
    allow_methods=["*"], # Permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"], # Permite todos los headers (incluyendo el de Authorization para el Token)
)

# Esto evita que el Swagger se congele si la DB tarda en responder
@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(boards.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "API Funcionando"}