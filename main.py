from fastapi import FastAPI
from routes.pacientes import pacientes
from config.db import Base, engine

app = FastAPI()

app.include_router(pacientes)
