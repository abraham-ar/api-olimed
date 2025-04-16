from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db import get_db
pacientes = APIRouter()

#Obtiene todos los pacientes
@pacientes.get("/pacientes")
def getPacientes(db: Session = Depends(get_db)):
    return "hola FastAPI"

#Registra un nuevo paciente
@pacientes.post("/pacientes/")
def getPaciente(id_paciente: int):
    return {"nombre": str(id_paciente)}

#Obtiene un paciente en especifico
@pacientes.get("/paciente/{id_paciente}")
def getPaciente(id_paciente: int):
    return {"nombre": str(id_paciente)}

#modifica un paciente
@pacientes.put("/paciente/{id_paciente}")
def getPaciente(id_paciente: int):
    return {"nombre": str(id_paciente)}

#elimina un paciente
@pacientes.delete("/paciente/{id_paciente}")
def getPaciente(id_paciente: int):
    return {"nombre": str(id_paciente)}