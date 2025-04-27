from fastapi import FastAPI
from routes import auth, pacientes
from config.db import Base, engine
import services

services.create_database()

app = FastAPI()

app.include_router(auth)
app.include_router(pacientes)
