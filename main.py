from fastapi import FastAPI
from routes import auth, pacientes, medicos, recepcionistas, fechas, citas, recetas
from config.db import Base, engine
from fastapi.middleware.cors import CORSMiddleware
import services

# Configura los orígenes permitidos en este caso donde se se encuentra en front
origins = [
    "http://localhost:3000",
]

services.create_database()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Qué orígenes pueden acceder
    allow_credentials=True, #permite envio de tokens JWT
    allow_methods=["*"],    # Qué métodos HTTP se permiten (GET, POST, PUT, etc)
    allow_headers=["*"],    # Qué cabeceras se permiten
)

app.include_router(auth)
app.include_router(pacientes)
app.include_router(medicos)
app.include_router(recepcionistas)
app.include_router(fechas)
app.include_router(recetas)
app.include_router(citas)