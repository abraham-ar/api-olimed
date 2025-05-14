from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db
import services as _services
from schemas.Medico import Medico, MedicoUpdate
from schemas.Notificacion_Admin import Notificacion_Admin
from models import Notificacion_Admin as Notificacion_db
from typing import List

medicos = APIRouter()

#Obtiene todos los medicos
@medicos.get("/medicos", response_model=List[Medico])
async def getMedicos(limit: int = 10, skip: int = 0, db: Session = Depends(get_db)):
    medicos = _services.get_medicos(limit=limit, skip=skip, db=db)
    return medicos

#Obtiene los datos de un medico en especifico
@medicos.get("/medico/{id_medico}", response_model=Medico)
async def getMedico(id_medico: int, db: Session = Depends(get_db)):
    medico = _services.get_medico_by_id(id_medico, db)

    if not medico:
        raise HTTPException(status_code=404, detail="Medico no encontrado")

    return medico

#modifica un medico
@medicos.put("/medico/{id_medico}", response_model=Medico)
async def modificaMedico(id_medico: int, medico_update: MedicoUpdate, db: Session = Depends(get_db)):
    medico_db = _services.get_medico_by_id(id_medico, db)

    if not medico_db:
        raise HTTPException(status_code=404, detail="Medico no encontrado")

    for key, value in medico_update.dict(exclude_unset=True).items():
        setattr(medico_db, key, value)

    db.commit()
    db.refresh(medico_db)
    return medico_db

#elimina un medico (verificar que no sea el unico registrado)
@medicos.delete("/medico/{id_medico}")
async def deleteMedico(id_medico: int, db: Session = Depends(get_db)):
    medico_db = _services.get_medico_by_id(id_medico, db)

    if not medico_db:
        raise HTTPException(status_code=404, detail="Medico no registrado")

    db.delete(medico_db)
    db.flush()
    db.commit()
    return {"message": "Medico eliminado"}

#obtiene las notificaciones del medico
@medicos.get("/medicos/{id_medico}/notificaciones", response_model=List[Notificacion_Admin])
async def getNotificaciones(id_medico: int, db: Session = Depends(get_db)):
    medico_db = _services.get_medico_by_id(id_medico, db)

    if not medico_db:
        raise HTTPException(status_code=404, detail="Medico no encontrado")
        
    return db.query(Notificacion_db).filter(Notificacion_db.idAdmin == id_medico).order_by(Notificacion_db.fecha_creacion.desc()).all()