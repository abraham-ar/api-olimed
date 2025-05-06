from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from config.db import get_db
import services as _services
from schemas.FechaDisponible import FechaDisponibleCreate, FechaDisponible, FechaDisponibleUpdate
from models import FechaDisponible as Fecha_db
from typing import List
from datetime import datetime, timedelta

fechas = APIRouter()

#permite crear una fecha Disponible para cita
@fechas.post("/fechasDisponibles")
async def createFechaDispnible(fechaNueva: FechaDisponibleCreate, db: Session = Depends(get_db)):
    fecha_db = _services.get_fechaDisponible_by_fecha(fechaNueva.fecha, db)

    if fecha_db: 
        raise HTTPException(status_code=400, detail="Ya hay una fecha creada para este dia y hora")

    fecha_obj = Fecha_db(
        fecha = fechaNueva.fecha,
        disponible = fechaNueva.disponible,
        seleccionado = fechaNueva.seleccionado        
    )

    db.add(fecha_obj)
    db.flush()
    db.commit()
    db.refresh(fecha_obj)
    return fecha_obj

#Obtiene todos las fechas disponiles para citas (puede devolver valores por defecto)
@fechas.get("/fechasDisponibles", response_model=List[FechaDisponible])
async def getFechasDisponibles(inicio: datetime = Query(None), fin: datetime = Query(None), db: Session = Depends(get_db)):
    if not inicio:
        inicio = datetime.now()

    if not fin:
        fin = inicio + timedelta(days=7)

    fechasDisponibles = _services.get_fechasDisponibles(inicio, fin, db)
    return fechasDisponibles

#modifica una fechaDisponible
@fechas.put("/fechaDisponible/{id_fecha}", response_model=FechaDisponible)
async def modificaFecha(id_fecha: int, fecha_update: FechaDisponibleUpdate, db: Session = Depends(get_db)):
    fecha_db = _services.get_recepcionista_by_id(id_fecha, db)

    if not fecha_db:
        raise HTTPException(status_code=404, detail="Fecha no encontrado")

    for key, value in fecha_update.dict(exclude_unset=True).items():
        setattr(fecha_db, key, value)

    db.commit()
    db.refresh(fecha_db)
    return fecha_db

@fechas.patch("/fechasDisponibles")
async def changeDisponible(inicio: datetime, fin: datetime, disponible: int, db: Session = Depends(get_db)):
    fechas = _services.get_fechasDisponibles(inicio, fin, db)

    for fecha in fechas:
        fecha.disponible = disponible
    
    db.commit()
    return {"message": "Disponibilidad de fechas actualizadas"}


@fechas.patch("/fechaDisponible/{id_fecha}")
async def changeSeleccionado(id_fecha: int, seleccionado: int, db: Session = Depends(get_db)):
    
    fecha_db = _services.get_fechaDisponible_by_id(id_fecha, db)

    if not fecha_db:
        raise HTTPException(status_code=404, detail="Ninguna fecha coincide con dicho id")
    
    fecha_db.seleccionado = seleccionado
    db.commit()
    return {"message": "Campo seleccionado actualizado"}

#elimina una fecha
@fechas.delete("/fechaDisponible/{id_fecha}")
async def deleteFechaDisponible(id_fecha: int, db: Session = Depends(get_db)):
    fecha_db = _services.get_fechaDisponible_by_id(id_fecha, db)

    if not fecha_db:
        raise HTTPException(status_code=404, detail="Ninguna fecha coincide con dicho id")

    db.delete(fecha_db)
    db.flush()
    db.commit()
    return {"message": "Fecha eliminada"}