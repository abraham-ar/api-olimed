from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db
import services as _services
from schemas.Paciente import PacienteForRecepcionista, Paciente, PacienteUpdate
from schemas.Paciente_Telefono import Paciente_TelefonoCreate, Paciente_TelefonoUpdate
from schemas.Alergia import AlergiaCreate, AlergiaUpdate
from schemas.Notificacion_Paciente import Notificacion_Paciente
from typing import List
from models import Paciente_Telefono as Telefono_db, Notificacion_Paciente as Notificacion_db
from models import Alergia as Alergia_db, Receta as Receta_db, Cita as Cita_db
from schemas.Receta import Receta
from schemas.Cita import Cita

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

    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    return paciente

#modifica un paciente (datos generales)
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


#agrega un telefono a un paciente
@pacientes.post("/paciente/{id_paciente}/telefono")
async def agregaTelefono(id_paciente: int, telefono: Paciente_TelefonoCreate, db: Session = Depends(get_db)):
    paciente_db = await _services.get_paciente_by_id(id_paciente, db)

    if not paciente_db:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    telefono_obj = Telefono_db(
        telefono = telefono.telefono,
        tipo = telefono.tipo,
        idPaciente = id_paciente
    )

    db.add(telefono_obj)
    db.commit()
    db.refresh(telefono_obj)
    return telefono_obj

#modificar un telefono de un paciente
@pacientes.put("/paciente/{id_paciente}/telefono/{id_telefono}")
async def modificaTelefono(id_paciente: int, id_telefono: int, telefono_update: Paciente_TelefonoUpdate , db: Session = Depends(get_db)):
    telefono_db = _services.get_telefono_by_id(id_telefono, db)

    if not telefono_db:
        raise HTTPException(status_code=404, detail="Ningun telefono coincide con dicho ID")
    
    if telefono_db.idPaciente != id_paciente:
        raise HTTPException(status_code="403", detail="Este telefono no pertenece al paciente especificado")
    
    for key, valor in telefono_update.dict(exclude_unset=True).items():
        setattr(telefono_db, key, valor)

    db.flush()
    db.commit()
    db.refresh(telefono_db)
    return telefono_db

#elimina un telefono de un paciente
@pacientes.delete("/paciente/{id_paciente}/telefono/{id_telefono}")
async def eliminaTelefono(id_paciente: int, id_telefono: int, db: Session = Depends(get_db)):
    telefono_db = _services.get_telefono_by_id(id_telefono, db)

    if not telefono_db:
        raise HTTPException(status_code=404, detail="Ningun telefono coincide con dicho ID")
    
    if telefono_db.idPaciente != id_paciente:
        raise HTTPException(status_code="403", detail="Este telefono no pertenece al paciente especificado")
    
    db.delete(telefono_db)
    db.flush()
    db.commit()
    return {"message": "Telefono eliminado"}


#agrega una alergia para un paciente
@pacientes.post("/paciente/{id_paciente}/alergia")
async def addAlergia(id_paciente: int, alergia: AlergiaCreate,db: Session = Depends(get_db)):
    paciente_db = await _services.get_paciente_by_id(id_paciente, db)

    if not paciente_db:
        raise HTTPException(status_code=404, detail="Ningun paciente coincide con el ID ingresado")
    
    alergia_obj = Alergia_db(
        nombre = alergia.nombre,
        idPaciente = id_paciente
    )

    db.add(alergia_obj)
    db.commit()
    db.refresh(alergia_obj)
    return alergia_obj

#modifica una alergia
@pacientes.put("/paciente/{id_paciente}/alergia/{id_alergia}")
async def modificaAlergia(id_paciente: int, id_alergia: int, alergia_update: AlergiaUpdate, db: Session = Depends(get_db)):
    alergia_db = _services.get_alergia_by_id(id_alergia, db)

    if not alergia_db:
        raise HTTPException(status_code=404, detail="Ningun registro coincide con el ID de la alergia ingresada")

    if alergia_db.idPaciente != id_paciente:
        raise HTTPException(status_code=403, detail="Esta alergia no pertenece al paciente especificado")

    for key, valor in alergia_update.dict(exclude_unset=True).items():
        setattr(alergia_db, key, valor)

    db.flush()
    db.commit()
    db.refresh(alergia_db)
    return alergia_db
    

#elimina una alergia de un paciente
@pacientes.delete("/paciente/{id_paciente}/alergia/{id_alergia}")
async def eliminaAlergia(id_paciente: int, id_alergia: int, db: Session = Depends(get_db)):
    alergia_db = _services.get_alergia_by_id(id_alergia, db)

    if not alergia_db:
        raise HTTPException(status_code=404, detail="Ningun registro coincide con el ID de la alergia ingresada")

    if alergia_db.idPaciente != id_paciente:
        raise HTTPException(status_code=403, detail="Esta alergia no pertenece al paciente especificado")

    db.delete(alergia_db)
    db.flush()
    db.commit()
    return {"message":"Alergia eliminada"}

#obtener notificaciones de paciente
@pacientes.get("/paciente/{id_paciente}/notificaciones", response_model=List[Notificacion_Paciente])
async def getNotificacion(id_paciente: int, db: Session = Depends(get_db)):
    paciente_db = await _services.get_paciente_by_id(id_paciente, db)

    if not paciente_db:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    notificaciones =  db.query(Notificacion_db).filter(Notificacion_db.idPaciente == id_paciente).order_by(Notificacion_db.fecha_creacion.desc()).all()
    return notificaciones

#obtener todas las proximas citas de un paciente
@pacientes.get("/pacientes/{id_paciente}/citas", response_model=List[Cita])
async def getCitasProximas(id_paciente: int, db: Session = Depends(get_db)):

    paciente_db = await _services.get_paciente_by_id(id_paciente, db)

    if not paciente_db:
        raise HTTPException(status_code=404, detail="Paciente no registrado")

    citas = _services.get_citas_proximas_by_paciente(id_paciente ,db)
    
    citas_resultado = List[Cita]
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

#obtiene todas las recetas de un paciente
@pacientes.get("/paciente/{id_paciente}/recetas", response_model=List[Receta])
async def obtenerRecetas(id_paciente: int, db: Session = Depends(get_db)):
    paciente_db = await _services.get_paciente_by_id(id_paciente, db)

    if not paciente_db:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    recetas = db.query(Receta_db).join(Cita_db).filter(Cita_db.idPaciente == id_paciente).order_by(Receta_db.fecha_creacion.desc()).all()
    
    return recetas