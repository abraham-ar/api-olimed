from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from config.db import get_db
import services as _services
from schemas.FechaDisponible import FechaDisponibleCreate, FechaDisponible, FechaDisponibleUpdate
from models import FechaDisponible as Fecha_db
from typing import List
from datetime import datetime, timedelta
from schemas.Notificacion_Admin import Notificacion_AdminCreate
from schemas.Notificacion_Paciente import Notificacion_PacienteCreate

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
    fecha_db = _services.get_fechaDisponible_by_id(id_fecha, db)

    if not fecha_db:
        raise HTTPException(status_code=404, detail="Fecha no encontrado")

    for key, value in fecha_update.dict(exclude_unset=True).items():
        setattr(fecha_db, key, value)

    db.commit()
    db.refresh(fecha_db)
    return fecha_db

#modifica la disponibilidad de un rango de fechas (es decir, las oculta o las muestre como activas)
@fechas.patch("/fechasDisponibles")
async def changeDisponible(inicio: datetime, fin: datetime, disponible: int, db: Session = Depends(get_db)):
    fechas = _services.get_fechasDisponibles(inicio, fin, db)

    for fecha in fechas:
        fecha.disponible = disponible
    
    db.commit()
    return {"message": "Disponibilidad de fechas actualizadas"}


#este endpoint cambia el estado de la seleccionado a 0 o 1 segun sea el caso, esto con el fin de marcar como seleccionado una fecha
#cuando un paciente la seleccione para una cita, o desmarcarla si cancela la creación de la cita
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
    mensaje = {}
    if not fecha_db:
        raise HTTPException(status_code=404, detail="Ninguna fecha coincide con dicho id")

    cita_asociada = fecha_db.Cita

    if cita_asociada: 
        notificacion = Notificacion_PacienteCreate(
            titulo="Cita eliminada debido a que se eliminó una Fecha",
            mensaje= f"Debido a que la Fecha disponible para el dia {fecha_db.fecha.date()} a las {fecha_db.fecha.time()} fue eliminada, tu cita para dicho día fue eliminada tambien",
            idPaciente=cita_asociada.idPaciente,
            fecnaCreacion=datetime.now(),
            tipoNotificacion="Sistema"
        )
        _services.create_notificacion_paciente(notificacion, db)

        #creación de la notificación para administrador
        notificacion_admin = Notificacion_AdminCreate(
            titulo="Cita cancelada",
            mensaje = f"Debido a que la Fecha disponible para el dia {fecha_db.fecha.date()} a las {fecha_db.fecha.time()} fue eliminada, la cita con el paciente {cita_asociada.Paciente.nombre} fue eliminada tambien",
            tipo="Sistema",
            fecha_creacion=datetime.now()
        )

        _services.create_notificacion_medico(notificacion_admin, db)

        db.delete(cita_asociada)
        db.commit()
        mensaje = {"message": "Fecha y cita eliminada"}
    
    db.delete(fecha_db)
    db.flush()
    db.commit()
    mensaje = {"message": "Fecha eliminada"}
    return mensaje