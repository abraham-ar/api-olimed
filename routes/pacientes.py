from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db
import services as _services
from schemas.Paciente import PacienteForRecepcionista, Paciente, PacienteUpdate
from typing import List

pacientes = APIRouter()

#Obtiene todos los pacientes
@pacientes.get("/pacientes", response_model=List[PacienteForRecepcionista])
async def getPacientes(limit: int = 10, skip: int = 0, db: Session = Depends(get_db)):
    pacientes = await _services.get_pacientes(limit=limit, skip=skip, db=db)
    return pacientes

#Obtiene un paciente en especifico
@pacientes.get("/paciente/{id_paciente}", response_model=Paciente)
async def getPaciente(id_paciente: int, db: Session = Depends(get_db)):
    paciente = await _services.get_paciente_by_id(id_paciente, db)
    return paciente

#modifica un paciente
@pacientes.put("/paciente/{id_paciente}", response_model=Paciente)
async def modificaPaciente(id_paciente: int, paciente_update: PacienteUpdate, db: Session = Depends(get_db)):
    paciente_db = await _services.get_paciente_by_id(id_paciente, db)

    if not paciente_db:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    for key, value in paciente_update.dict(exclude_unset=True).items():
        setattr(paciente_db, key, value)

    db.commit()
    db.refresh(paciente_db)
    return paciente_db

#elimina un paciente
@pacientes.delete("/paciente/{id_paciente}")
async def deletePaciente(id_paciente: int, db: Session = Depends(get_db)):
    paciente_db = await _services.get_paciente_by_id(id_paciente, db)

    if not paciente_db:
        raise HTTPException(status_code=404, detail="Paciente no registrado")

    db.delete(paciente_db)
    db.flush()
    db.commit()
    return {"message": "Paciente eliminado"}