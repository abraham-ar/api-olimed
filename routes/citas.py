from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from config.db import get_db
import services as _services
from schemas.Cita import CitaCreate, Cita
from schemas.Cita_Sintoma import Cita_SintomaCreate
from schemas import Cita_Sintoma as Cita_SintomaSchema
from models import Cita as Cita_db
from models import Cita_Sintoma
from datetime import datetime, date
from schemas.Notificacion_Paciente import Notificacion_PacienteCreate
from schemas.Notificacion_Admin import Notificacion_AdminCreate
from typing import List
from datetime import datetime

citas = APIRouter()

@citas.get("/citas/{actuales}", response_model=List[Cita])
async def getCitas(actuales: int, db: Session = Depends(get_db)):

    if actuales == 0:
        citas = _services.get_citas(db)
    else:
        fecha_actual = datetime.now()
        citas = _services.get_citas_activas(fecha_actual ,db)
    print(len(citas))

    citas_resultado = []
    for cita in citas:
        citas_resultado.append(
            Cita(
                idCita=cita.idCita,
                fecha=cita.Fecha.fecha,
                idPaciente=cita.idPaciente,
                estado = cita.estado,
                Sintomas = cita.Sintomas,
                idFecha = cita.idFecha
            )
        )

    return citas_resultado

#creación de citas
@citas.post("/citas")
async def addCita(cita: CitaCreate, db: Session = Depends(get_db)):
    print("Check 1")
    #comprueba que la fechaDisponible exista
    fecha_db = _services.get_fechaDisponible_by_id(cita.idFecha, db)
    if not fecha_db:
        raise HTTPException(status_code=404, detail="Fecha no encontrada")
    
    if fecha_db.disponible == 0:
        raise HTTPException(status_code=400, detail="La fecha ya no está disponible")
    
    #modificar el estado de la fecha para marcarla como no disponible
    fecha_db.disponible = 0
    db.commit()

    #comprueba la existencia del paciente
    paciente_db = _services.get_pacienteSimple_by_id(cita.idPaciente, db)
    if not paciente_db:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    #obtenemos los sintomas ya que se crearan registros en otra tabla
    sintomas = cita.Sintomas

    #cambiamos el valor a None para que no se asigne al objeto Cita que vamos a crear
    cita.Sintomas = None

    #creación e inicialización del objeto cita
    cita_obj = Cita_db()
    
    data  = cita.dict(exclude_unset=True)
    data.pop("Sintomas")

    for key, value in data.items():
        setattr(cita_obj, key, value)
    print("Lllega hasta esta linea")
    #creacion del registro en la bd
    db.add(cita_obj)
    db.commit()
    db.refresh(cita_obj)

    #creación de los sintomas asociados a la cita
    for sintoma in sintomas:
        sintoma_obj = Cita_Sintoma(
            idCita = cita_obj.idCita,
            sintoma = sintoma.sintoma
        )
        db.add(sintoma_obj)
        db.commit()
    
    #creación de la notificacion para el paciente
    notificacion = Notificacion_PacienteCreate(
        titulo="Nueva cita agendada",
        mensaje= f"Tu cita fue agendada para el dia {fecha_db.fecha.date()} a las {fecha_db.fecha.time()}",
        idPaciente=cita.idPaciente,
        fecnaCreacion=datetime.now(),
        tipoNotificacion="Sistema"
    )
    _services.create_notificacion_paciente(notificacion, db)
    #creación de la notificación para administrador
    notificacion_admin = Notificacion_AdminCreate(
        titulo="Nueva cita agendada",
        idAdmin=1,
        mensaje = f"El paciente {paciente_db.nombre} ha agendado una cita para el dia {fecha_db.fecha.date()} a las {fecha_db.fecha.time()}.",
        tipo="Sistema",
        fecha_creacion=datetime.now()
    )

    _services.create_notificacion_medico(notificacion_admin, db)

    #retorno de la inserción de la cita en la BD
    db.refresh(cita_obj)
    return cita_obj

@citas.delete("/cita/{id_cita}")
async def deleteCita(id_cita: int, db: Session = Depends(get_db)):

    cita_db = db.query(Cita_db).options(
        selectinload(Cita_db.Paciente),
        selectinload(Cita_db.Fecha)
    ).filter(Cita_db.idCita == id_cita).first()

    if not cita_db:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    
    #cambiamos el estado de la Fecha para que vuelva a aparecer como disponible
    cita_db.Fecha.seleccionado = 0
    cita_db.Fecha.disponible = 1

    notificacion = Notificacion_PacienteCreate(
        titulo="Cita eliminada",
        mensaje= f"Tu cita para el dia {cita_db.Fecha.fecha.date()} a las {cita_db.Fecha.fecha.time()} fue eliminada",
        idPaciente=cita_db.idPaciente,
        fecnaCreacion=datetime.now(),
        tipoNotificacion="Sistema"
    )
    _services.create_notificacion_paciente(notificacion, db)

    #creación de la notificación para administrador
    notificacion_admin = Notificacion_AdminCreate(
        titulo="Cita cancelada",
        mensaje = f"El paciente {cita_db.Paciente.nombre} ha cancelado su cita para el dia {cita_db.Fecha.fecha.date()} a las {cita_db.Fecha.fecha.time()}",
        tipo="Sistema",
        fecha_creacion=datetime.now()
    )

    _services.create_notificacion_medico(notificacion_admin, db)

    db.delete(cita_db)
    db.commit()
    return {"message": "Cita eliminada"}

@citas.get("/citas/{id_cita}/sintomas", response_model=List[Cita_SintomaSchema])
async def get_sintomas_de_cita(id_cita: int, db: Session = Depends(get_db)):
    cita = db.query(Cita).filter(Cita.idCita == id_cita).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    
    return cita.Sintomas

@citas.post("/citas/{id_cita}/sintomas", response_model=Cita_SintomaSchema)
async def addSintomaToCita(id_cita: int, sintoma: Cita_SintomaCreate, db: Session = Depends(get_db)):

    # Verifica si la cita existe
    cita_db = _services.get_cita_by_id(id_cita, db)
    if not cita_db:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    # Crea el nuevo síntoma vinculado a la cita
    nuevo_sintoma = Cita_Sintoma(
        idCita=id_cita,
        sintoma=sintoma.sintoma
    )

    db.add(nuevo_sintoma)
    db.commit()
    db.refresh(nuevo_sintoma)

    return nuevo_sintoma