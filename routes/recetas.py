from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from config.db import get_db
import services as _services
from schemas.Receta import RecetaCreate, Receta, RecetaUpdate
from models import Receta as Receta_db

recetas = APIRouter()

#Guarda una receta
@recetas.post("/receta")
async def addReceta(receta: RecetaCreate, db: Session = Depends(get_db)):
    cita_db = _services.get_cita_by_id(receta.idCita, db)

    if not cita_db:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    #modificamos la cita para cambiar su estado a 0 y con ello marcarla como ya hecha
    cita_db.estado = 0

    receta_obj = Receta_db()

    for key, value in receta.dict(exclude_unset=True).items():
        setattr(receta_obj, key, value)

    db.add(receta_obj)
    db.commit()
    db.refresh(receta_obj)
    return receta_obj

#elimina una receta
@recetas.delete("/receta/{id_receta}")
async def deleteReceta(id_receta: int, cambiarEstado: int = Query(None), db: Session = Depends(get_db)):
    receta_db = _services.get_receta_by_id(id_receta, db)

    if not receta_db:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    
    #esto para cambiar como que la Cita aun no se procesa
    if cambiarEstado:
        receta_db.Cita.estado = 1

    db.delete(receta_db)
    db.commit()
    return {"message": "Receta eliminada"}

@recetas.put("/receta/{id_receta}")
async def updateReceta(id_receta: int, receta_update: RecetaUpdate, db: Session = Depends(get_db)):
    receta_db = _services.get_receta_by_id(id_receta, db)

    if not receta_db:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    
    for key, value in receta_update.dict(exclude_unset=True).items():
        setattr(receta_db, key, value)

    db.commit()
    db.refresh(receta_db)
    return receta_db
    