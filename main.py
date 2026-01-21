from fastapi import FastAPI
from database import engine
import models
from routers import users, boards, auth

app = FastAPI(title="Trello Clone API")

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