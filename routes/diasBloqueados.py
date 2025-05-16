from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from config.db import get_db
import services as _services
from schemas.Cita import CitaCreate, Cita
from models import Cita as Cita_db
from models import Cita_Sintoma
from datetime import datetime, date
from schemas.Notificacion_Paciente import Notificacion_PacienteCreate
from schemas.Notificacion_Admin import Notificacion_AdminCreate
from typing import List
from datetime import datetime

diasBloqueados = APIRouter()

@diasBloqueados.get("/diasBloqueados")
async def getDiasBloqueados(db: Session = Depends(get_db)):
    diasBloqueados = _services.get_dias_bloqueados(db)
    
    return [d.isoformat() for d in diasBloqueados]