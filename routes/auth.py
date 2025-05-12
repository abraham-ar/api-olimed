from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from config.db import get_db
from schemas.Admin import AdminLogin
from schemas.Medico import *
from schemas.Paciente import *
from schemas.Recepcionista import *
from models import CuentaAdmin, CuentaPaciente, CuentaRecepcionista, Cita, Paciente_Telefono, Alergia
from passlib.hash import bcrypt
from datetime import datetime
import services as _services
from services import get_current_medico
from services import get_current_paciente

auth = APIRouter()

@auth.post("/auth/register/recepcionistas")
async def registerRecepcionista(recepcionista: RecepcionistaCreate, db: Session = Depends(get_db)):
    db_recepcionista = await _services.get_recepcionista_by_email(recepcionista.correo, db)

    if db_recepcionista:
        raise HTTPException(status_code=400, detail="Correo ya registrado")
    
    #generar clave de inicio de sesion
    clave_sesion = await _services.generar_clave_recepcionista(db=db)

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
    db_paciente = await _services.get_paciente_by_email(paciente.correo, db)

    if db_paciente:
        raise HTTPException(status_code=400, detail="Correo ya registrado")

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

@auth.post("/auth/login/medicos")
async def loginMedico(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    medico = await _services.authenticate_medico(form_data.username, form_data.password, db)

    if not medico:
        raise HTTPException(status_code=401, detail="Credenciales del medico no validas")
    
    return await _services.create_token(data={"sub": str(medico.idAdmin), "role": "medico"})

@auth.post("/auth/login/recepcionistas")
async def loginRecepcionista(form_data: OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):
    recepcionista = await _services.authenticate_recepcionista(form_data.username, form_data.password, db)

    if not recepcionista:
        raise HTTPException(status_code=401, detail="Credenciales del recepcionista no validas")
    
    return await _services.create_token(data={"sub": str(recepcionista.idRecepcionista), "role": "recepcionista"})

@auth.post("/auth/login/pacientes")
async def loginPaciente(form_data: OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):
    paciente = await _services.authenticate_paciente(form_data.username, form_data.password, db)

    if not paciente:
        raise HTTPException(status_code=401, detail="Credenciales del paciente no validas")
    
    return await _services.create_token(data={"sub": str(paciente.idPaciente), "role": "paciente"})

@auth.patch("/auth/change-password/medico")
async def changePasswordMedico(passwords: MedicoUpdatePassword, db: Session = Depends(get_db), current_medico: CuentaAdmin = Depends(get_current_medico)):
    if not current_medico:
        print("Medico no encontrado")
        raise HTTPException(status_code=401, detail="No autorizado para esta acción")
    
    if not current_medico.verify_password(passwords.current_password):
        print("Contraseña incorrecta")
        raise HTTPException(status_code=401, detail="No autorizado")
    
    current_medico.hashed_password = bcrypt.hash(passwords.new_password)

    db.commit()
    db.refresh(current_medico)
    return {"message": "Contraseña modificada con exito"}

@auth.patch("/auth/change-password/paciente")
async def changePasswordPaciente(passwords: PacienteUpdatePassword, current_paciente: CuentaPaciente = Depends(get_current_paciente),db: Session = Depends(get_db)):
    if not current_paciente:
        print("Paciente no encontrado")
        raise HTTPException(status_code=401, detail="No autorizado para esta acción")
    
    if not current_paciente.verify_password(passwords.current_password.get_secret_value()):
        print("Contraseña incorrecta")
        raise HTTPException(status_code=401, detail="No autorizado")
    
    current_paciente.hashed_password = bcrypt.hash(passwords.new_password.get_secret_value())

    db.commit()
    db.refresh(current_paciente)
    return {"message": "Contraseña modificada con exito"}

@auth.patch("/auth/recover-password/paciente")
async def recoverPasswordPaciente(paciente_recover: PacienteRecoverPassword, db: Session = Depends(get_db)):
    paciente_db = await _services.get_paciente_by_email(paciente_recover.correo, db)

    if not paciente_db:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    if paciente_db.nombre != paciente_recover.nombre:
        raise HTTPException(status_code=401 ,detail="El nombre es incorrecto")
    
    paciente_db.hashed_password = bcrypt.hash(paciente_recover.new_password.get_secret_value())
    return {"message": "La contraseña se ha cambiado con exito"}