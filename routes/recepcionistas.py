from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db
import services as _services
from schemas.Recepcionista import Recepcionista, RecepcionistaSimple, RecepcionistaUpdate
from typing import List

recepcionistas = APIRouter()

#Obtiene todos los recepcionistas
@recepcionistas.get("/recepcionistas", response_model=List[RecepcionistaSimple])
async def getRecepcionistas(limit: int = 10, skip: int = 0, db: Session = Depends(get_db)):
    recepcionistas = _services.get_recepcionistas(limit=limit, skip=skip, db=db)
    return recepcionistas

#Obtiene un recepcionista en especifico
@recepcionistas.get("/recepcionista/{id_recepcionista}", response_model=Recepcionista)
async def getMedico(id_recepcionista: int, db: Session = Depends(get_db)):
    recepcionista = _services.get_recepcionista_by_id(id_recepcionista, db)

    if not recepcionista:
        raise HTTPException(status_code=404, detail="Recepcionista no encontrado")

    return recepcionista

#modifica un recepcionista
@recepcionistas.put("/recepcionista/{id_recepcionista}", response_model=Recepcionista)
async def modificaMedico(id_recepcionista: int, recepcionista_update: RecepcionistaUpdate, db: Session = Depends(get_db)):
    recepcionista_db = _services.get_recepcionista_by_id(id_recepcionista, db)

    if not recepcionista_db:
        raise HTTPException(status_code=404, detail="Recepcionista no encontrado")

    for key, value in recepcionista_update.dict(exclude_unset=True).items():
        setattr(recepcionista_db, key, value)

    db.commit()
    db.refresh(recepcionista_db)
    return recepcionista_db

#elimina un recepcionista
@recepcionistas.delete("/recepcionista/{id_recepcionista}")
async def deleteRecepcionista(id_recepcionista: int, db: Session = Depends(get_db)):
    recepcionista_db = _services.get_recepcionista_by_id(id_recepcionista, db)

    if not recepcionista_db:
        raise HTTPException(status_code=404, detail="Recepcionista no registrado")

    db.delete(recepcionista_db)
    db.flush()
    db.commit()
    return {"message": "Recepcionista eliminado"}