from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from config.db import get_db
import services as _services
from schemas.FechaDisponible import FechaDisponibleCreate, FechaDisponible, FechaDisponibleUpdate
from models import FechaDisponible as Fecha_db
from typing import List
from datetime import datetime, timedelta, date
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
        bloqueado = fechaNueva.bloqueado
    )

    db.add(fecha_obj)
    db.flush()
    db.commit()
    db.refresh(fecha_obj)
    return fecha_obj

#obtiene las horas disponibles para cita de acuerdo al dia enviado
@fechas.get("/fechasDisponibles", response_model=List[FechaDisponible])
async def getFechasDisponiblesByDia(fecha: date, db: Session = Depends(get_db)):
    horario = _services.get_horario_by_dia(fecha, db)

    return horario

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

#bloquea o desbloquea un rango de dias
@fechas.patch("/fechasDisponibles")
async def changeBloqueado(inicio: datetime, fin: datetime, bloqueado: int, db: Session = Depends(get_db)):
    fechas = _services.get_fechas_by_rango(inicio, fin, db)

    mensaje = ""

    if bloqueado == 1:
        #verificar que los dias a bloquear no esten dentro del rango de dias ya bloqueados
        dias_bloqueados = _services.get_dias_bloqueados(db)

        fecha_inicio = inicio.date()
        fecha_fin = fin.date()

        fechas_a_bloquear = []

        current = fecha_inicio
        while current <= fecha_fin:
            fechas_a_bloquear.append(current)
            current += timedelta(days=1)

        for dia in dias_bloqueados:
            if dia in fechas_a_bloquear:
                raise HTTPException(status_code=401, detail="El rango de dias a bloquear contiene dia(s) ya bloqueado(s)")

        #falta programar logica de verificar las citas asignadas a estos dias
        citas = _services.get_citas_by_rango(inicio, fin, db)

        for cita in citas:
            notificacion = Notificacion_PacienteCreate(
                titulo="Cita eliminada debido a que ese dia no habra servicio",
                mensaje= f"Debido a que la Fecha disponible para el dia {cita.Fecha.fecha.date()} a las {cita.Fecha.fecha.time()} fue bloqueada, tu cita para dicho día fue eliminada",
                idPaciente=cita.idPaciente,
                fecnaCreacion=datetime.now(),
                tipoNotificacion="Sistema"
            )
            _services.create_notificacion_paciente(notificacion, db)

            #creación de la notificación para administrador
            notificacion_admin = Notificacion_AdminCreate(
                titulo="Cita cancelada por bloquea de fechas",
                mensaje = f"Debido a que bloqueaste el dia {cita.Fecha.fecha.date()}, la cita con el paciente {cita.Paciente.nombre} fue eliminada",
                tipo="Sistema",
                fecha_creacion=datetime.now()
            )

            _services.create_notificacion_medico(notificacion_admin, db)

            db.delete(cita)

        mensaje = "Dias bloqueados con exito"
        
    else:
        mensaje = "Dias desbloqueados con exito"
    
    for fecha in fechas:
        print("Bloqueando dias")
        fecha.bloqueado = bloqueado
    
    db.commit()
    return {"message": mensaje}


#este endpoint marca como disponible o no disponible una fecha
@fechas.patch("/fechaDisponible/{id_fecha}")
async def changeSeleccionado(id_fecha: int, disponible: int, db: Session = Depends(get_db)):
    
    fecha_db = _services.get_fechaDisponible_by_id(id_fecha, db)

    if not fecha_db:
        raise HTTPException(status_code=404, detail="Ninguna fecha coincide con dicho id")
    
    if fecha_db.disponible == 0 and disponible == 0:
        raise HTTPException(status_code=401, detail="La fecha ya fue seleccionada por otra persona")

    fecha_db.disponible = disponible
    db.commit()
    return {"message": "Disponibilidad de la fecha actualizada"}

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