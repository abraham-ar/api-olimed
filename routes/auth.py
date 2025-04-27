from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db
from schemas.Admin import AdminLogin
from schemas.Medico import *
from schemas.Paciente import *
from schemas.Recepcionista import *
from models import CuentaAdmin, CuentaPaciente, CuentaRecepcionista, Cita, Paciente_Telefono, Alergia
from passlib.hash import bcrypt
from datetime import datetime

def generar_clave(db: Session) -> str:
    year_actual = datetime.now().year % 100

    last_recepcionista = db.query(CuentaRecepcionista).order_by(CuentaRecepcionista.idRecepcionista.desc()).first()

    if last_recepcionista:
        secuencia = last_recepcionista.idRecepcionista + 1
    else:
        secuencia = 1

    secuencia_str = str(secuencia).zfill(4)

    clave = f"{year_actual}{secuencia_str}"

    return clave

auth = APIRouter()

@auth.post("/auth/register/recepcionistas")
async def registerRecepcionista(recepcionista: RecepcionistaCreate, db: Session = Depends(get_db)):
    db_recepcionista = db.query(CuentaRecepcionista).filter(CuentaRecepcionista.correo == recepcionista.correo).first()
    if db_recepcionista:
        raise HTTPException(status_code=400, detail="Correo ya registrado")
    
    #generar clave de inicio de sesion
    clave_sesion = generar_clave(db=db)

    recepcionista_obj = CuentaRecepcionista(
        nombre = recepcionista.nombre,
        clave = clave_sesion,
        correo = recepcionista.correo,
        telefono = recepcionista.telefono,
        hashed_password = bcrypt.hash(recepcionista.password.get_secret_value())
    )
    db.add(recepcionista_obj)
    db.flush()
    db.commit()
    db.refresh(recepcionista_obj)
    return recepcionista_obj


@auth.post("/auth/register/pacientes")
async def registerPaciente(paciente: PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = db.query(CuentaPaciente).filter(CuentaPaciente.correo == paciente.correo).first()

    if db_paciente:
        HTTPException(status_code=400, detail="Correo ya registrado")

    paciente_obj = CuentaPaciente(
        correo = paciente.correo,
        hashed_password = bcrypt.hash(paciente.password.get_secret_value()),
        nombre = paciente.nombre,
        fecha_nacimiento = paciente.fecha_nacimiento
    )

    db.add(paciente_obj)
    db.flush()
    db.commit()
    db.refresh(paciente_obj)
    return paciente_obj

@auth.post("/auth/login/admin")
async def loginAdmin(admin: AdminLogin ,db: Session = Depends(get_db)):
    pass

@auth.post("/auth/login/pacientes")
async def loginPaciente(db: Session = Depends(get_db)):
    pass