from fastapi import FastAPI
from routes.pacientes import pacientes
from config.db import Base, engine
import services

services.create_database()

app = FastAPI()

app.include_router(pacientes)
