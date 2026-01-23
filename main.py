from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from routers import users, boards, auth, lists, cards

app = FastAPI(title="Trello Clone API")

origins = [
    "http://localhost",
    "http://localhost:3000", # Puerto común de React
    "http://localhost:5173", # Puerto común de Vite/Vue
    "*", # EL COMODÍN: Permite cualquier origen (útil para pruebas, pero úsalo con cuidado)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Permite estos orígenes
    allow_credentials=True,
    allow_methods=["*"],              # Permite todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],              # Permite todos los headers (incluyendo Authorization)
)

# Esto evita que el Swagger se congele si la DB tarda en responder
@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(boards.router)
app.include_router(lists.router)
app.include_router(cards.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "API Funcionando"}