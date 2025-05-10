from fastapi import FastAPI, Depends
from routes import auth, pacientes, medicos, recepcionistas, fechas, citas, recetas
from config.db import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from models import CuentaAdmin
from fastapi.middleware.cors import CORSMiddleware
import services
from passlib.hash import bcrypt
import logging

#creación del usuario Admin
def crear_usuario_principal():
    db: Session = SessionLocal()
    try:
        admin = db.query(CuentaAdmin).filter(CuentaAdmin.clave == "251001").first()
        if not admin:
            nuevo_admin = CuentaAdmin(
                nombre="Dr. Oliver Pichardo",
                clave="251001",
                hashed_password = bcrypt.hash("Oliver_123"),
            )
            db.add(nuevo_admin)
            db.commit()
            logging.info("Administrador principal creado.")
        else:
            logging.info("Administrador principal ya existe.")
    finally:
        db.close()

# Configura los orígenes permitidos en este caso donde se se encuentra en front
origins = [
    "http://localhost:3000",
]

services.create_database()

crear_usuario_principal()

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