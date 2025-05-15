from config.db import Base, engine
from sqlalchemy.orm import Session, selectinload, joinedload
from models import CuentaAdmin, CuentaRecepcionista, CuentaPaciente, Alergia , Paciente_Telefono, Notificacion_Paciente, Cita, Cita_Sintoma, Receta, FechaDisponible, Notificacion_Admin
from schemas.Paciente import Paciente
from schemas.Notificacion_Paciente import Notificacion_PacienteCreate
from schemas.Notificacion_Admin import Notificacion_AdminCreate
from datetime import datetime, timedelta, date
import jwt as _jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from config.db import get_db
from sqlalchemy import func

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

JWT_SECRET = "myjwtsecret"
ACCESS_TOKEN_EXPIRE = 30

def create_database():
    return Base.metadata.create_all(bind=engine)

#metodos para obtener los registros de cuentapaciente
async def get_paciente_by_email(correo: str,db: Session) -> CuentaPaciente:
    paciente = db.query(CuentaPaciente).filter(CuentaPaciente.correo == correo).first()
    return paciente

async def get_paciente_by_id(id: int, db: Session):
    return db.query(CuentaPaciente)\
        .options(
            selectinload(CuentaPaciente.Alergias),
            selectinload(CuentaPaciente.Telefonos)
        )\
        .filter(CuentaPaciente.idPaciente == id)\
        .first()

def get_pacienteSimple_by_id(id: int, db: Session):
    return db.query(CuentaPaciente).filter(CuentaPaciente.idPaciente == id).first()
    

async def get_pacientes(limit: int, skip: int, db: Session):
    return db.query(CuentaPaciente).order_by(CuentaPaciente.nombre).offset(skip).limit(limit).all()


#operaciones con telefonos de pacientes
def get_telefono_by_id(id: int, db: Session):
    return db.query(Paciente_Telefono).filter(Paciente_Telefono.id == id).first()


#operaciones con alergias de pacientes
def get_alergia_by_id(id: int, db: Session):
    return db.query(Alergia).filter(Alergia.id == id).first()


#metodos para devolver los registros de cuentarecepcionista
def get_recepcionistas(limit: int, skip: int, db: Session):
    return db.query(CuentaRecepcionista).order_by(CuentaRecepcionista.nombre).offset(skip).limit(limit).all()

async def get_recepcionista_by_email(correo: str,db: Session):
    return db.query(CuentaRecepcionista).filter(CuentaRecepcionista.correo == correo).first()

async def get_recepcionista_by_clave(clave: str, db: Session):
    return db.query(CuentaRecepcionista).filter(CuentaRecepcionista.clave == clave).first()

def get_recepcionista_by_id(id: str, db: Session):
    return db.query(CuentaRecepcionista).filter(CuentaRecepcionista.idRecepcionista == id).first()


#metodos para devolver los registros de cuentaAdmin
async def get_medico_by_clave(clave: str, db: Session):
    return db.query(CuentaAdmin).filter(CuentaAdmin.clave == clave).first()

def get_medico_by_id(id: int, db: Session):
    return db.query(CuentaAdmin).filter(CuentaAdmin.idAdmin == id).first()

def get_medicos(limit: int, skip: int, db:Session):
    return db.query(CuentaAdmin).order_by(CuentaAdmin.nombre).offset(skip).limit(limit).all()

#metodo para obtener registros de FechasDisponibles
def get_fechasDisponibles(inicio: datetime, fin: datetime, db: Session):
    return db.query(FechaDisponible).filter(FechaDisponible.fecha >= inicio,
                                            FechaDisponible.fecha <= fin, 
                                            FechaDisponible.disponible == 1,
                                            FechaDisponible.seleccionado == 0).order_by(FechaDisponible.fecha).all()

def get_horario_by_dia(fecha: date, db: Session):
    return db.query(FechaDisponible).filter(func.date(FechaDisponible.fecha) == fecha).order_by(FechaDisponible.fecha).all()

def get_fechaDisponible_by_fecha(fecha: datetime, db: Session):
    return db.query(FechaDisponible).filter(FechaDisponible.fecha == fecha).first()

def get_fechaDisponible_by_id(id: int, db: Session):
    return db.query(FechaDisponible).filter(FechaDisponible.idFecha == id).first()


#metodos para Citas
def get_cita_by_id(id: int, db: Session):
    return db.query(Cita).filter(Cita.idCita == id).first()

def get_citas(db: Session):
     return db.query(Cita).join(Cita.Fecha).options(joinedload(Cita.Fecha)).order_by(FechaDisponible.fecha.asc()).all()

def get_citas_activas(fecha: datetime ,db: Session):
    return db.query(Cita).join(Cita.Fecha).options(joinedload(Cita.Fecha)).filter(Cita.estado == 1, FechaDisponible.fecha >= fecha).order_by(FechaDisponible.fecha).all()

#metodos para recetas
def get_receta_by_id(id: int, db: Session):
    return db.query(Receta).filter(Receta.idCita == id).first()

#metodos para notificaciones de paciente
def create_notificacion_paciente(notificacion: Notificacion_PacienteCreate, db: Session):
    notificacion_obj = Notificacion_Paciente(
        idPaciente = notificacion.idPaciente,
        tipoNotificacion = notificacion.tipoNotificacion,
        titulo= notificacion.titulo,
        mensaje = notificacion.mensaje,
        fecha_creacion = notificacion.fecnaCreacion
    )

    db.add(notificacion_obj)
    db.commit()

def get_citas_proximas_by_paciente(id: int, db: Session):
        fecha = datetime.now()
        return db.query(Cita).join(Cita.Fecha).options(joinedload(Cita.Fecha)).filter(Cita.estado == 1, Cita.idPaciente == id, FechaDisponible.fecha >= fecha).order_by(FechaDisponible.fecha).all()

#metodos para notificaciones de administrador
def create_notificacion_medico(notificacion: Notificacion_AdminCreate, db: Session):
    notifciacion_obj = Notificacion_Admin()
    for key, value in notificacion.dict(exclude_none=True).items():
        setattr(notifciacion_obj, key, value)
    
    db.add(notifciacion_obj)
    db.commit()

#metodo para generar la clave del recepcionista
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


#metodos de autenticación para los 3 usuarios
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

#metodo usado para crear el JWT
async def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    to_encode.update({"exp": expire})
    token = _jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")

    return dict(access_token = token, token_type="bearer")


def get_current_medico(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    
    try:
        decoded = _jwt.decode(token, options={"verify_signature": False})
        print(datetime.fromtimestamp(decoded["exp"]))
        payload = _jwt.decode(token, JWT_SECRET, algorithms="HS256")
        medico_id: int = payload.get("sub")
        role: str = payload.get("role")
    except _jwt.ExpiredSignatureError:
        print("token expirado")
        raise HTTPException(status_code=401, detail="Token expirado")
    except _jwt.InvalidTokenError:
        print("token invalido")
        raise HTTPException(status_code=401, detail="Token inválido")

    if not role == "medico":
        print("El usuario no es un medico")
        raise HTTPException(status_code=401, detail="El usuario no es un medico")

    medico = get_medico_by_id(medico_id, db)

    if medico is None:
        print("medico no encontrado en la BD")
        raise HTTPException(status_code=404, detail="Médico no encontrado")

    return medico

def get_current_paciente(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        decoded = _jwt.decode(token, options={"verify_signature": False})
        print(datetime.fromtimestamp(decoded["exp"]))
        payload = _jwt.decode(token, JWT_SECRET, algorithms="HS256")
        paciente_id: int = payload.get("sub")
        role: str = payload.get("role")
    except _jwt.ExpiredSignatureError:
        print("token expirado")
        raise HTTPException(status_code=401, detail="Token expirado")
    except _jwt.InvalidTokenError:
        print("token invalido")
        raise HTTPException(status_code=401, detail="Token inválido")

    if not role == "paciente":
        print("El usuario no es un paciente")
        raise HTTPException(status_code=401, detail="El usuario no es un paciente")

    paciente = db.query(CuentaPaciente).filter(CuentaPaciente.idPaciente == paciente_id).first()

    if not paciente:
        print("medico no encontrado en la BD")
        raise HTTPException(status_code=404, detail="Médico no encontrado")

    return paciente