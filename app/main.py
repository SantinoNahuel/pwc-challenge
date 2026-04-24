from fastapi import FastAPI
from . import models, database
from .routers import clients

# 1. Crea las tablas en SQLite si no existen
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="PwC Client Challenge API")

# 2. Registramos el router que acabamos de crear
app.include_router(clients.router)

@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}


