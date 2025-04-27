from config.db import Base, engine
from sqlalchemy.orm import Session
from models import CuentaAdmin, CuentaRecepcionista, CuentaPaciente, Alergia , Paciente_Telefono, Notificacion_Paciente, Cita, Cita_Sintoma, Receta, FechaDisponible, Notificacion_Admin
from schemas.Paciente import PacienteLogin, Paciente
from datetime import datetime, timedelta
import jwt as _jwt

JWT_SECRET = "myjwtsecret"
ACCESS_TOKEN_EXPIRE = 30

def create_database():
    return Base.metadata.create_all(bind=engine)

async def get_paciente_by_email(correo: str,db: Session):
    return db.query(CuentaPaciente).filter(CuentaPaciente.correo == correo).first()

async def get_recepcionista_by_email(correo: str,db: Session):
    return db.query(CuentaRecepcionista).filter(CuentaRecepcionista.correo == correo).first()

async def get_recepcionista_by_clave(clave: str, db: Session):
    return db.query(CuentaRecepcionista).filter(CuentaRecepcionista.clave == clave).first()

async def get_medico_by_clave(clave: str, db: Session):
    return db.query(CuentaAdmin).filter(CuentaAdmin.clave == clave).first()

async def generar_clave_recepcionista(db: Session) -> str:
    year_actual = datetime.now().year % 100

    last_recepcionista = db.query(CuentaRecepcionista).order_by(CuentaRecepcionista.idRecepcionista.desc()).first()

    if last_recepcionista:
        secuencia = last_recepcionista.idRecepcionista + 1
    else:
        secuencia = 1

    secuencia_str = str(secuencia).zfill(3)

    clave = f"{year_actual}2{secuencia_str}"

    return clave

async def authenticate_medico(clave: str, password: str, db: Session):
    medico_db = await get_medico_by_clave(clave, db)

    if not medico_db:
        return False
    
    if not medico_db.verify_password(password):
        return False
    
    return medico_db

async def authenticate_recepcionista(clave: str, password: str, db: Session):
    recepcionista_db = await get_recepcionista_by_clave(clave, db)

    if not recepcionista_db:
        return False
    
    if not recepcionista_db.verify_password(password):
        return False
    
    return recepcionista_db

async def authenticate_paciente(correo: str, password: str, db: Session):
    paciente_db = await get_paciente_by_email(correo, db)

    if not paciente_db:
        return False
    
    if not paciente_db.verify_password(password):
        return False
    
    return paciente_db

async def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    to_encode.update({"exp": expire})
    token = _jwt.encode(to_encode, JWT_SECRET)

    return dict(access_token = token, token_type="bearer")