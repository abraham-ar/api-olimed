from pydantic import BaseModel
from typing import List
from datetime import datetime
from .Cita_Sintoma import Cita_Sintoma, Cita_SintomaCreate

class _CitaBase(BaseModel):
    estado: int

class CitaCreate(_CitaBase):
    idFecha: int #si o si necesario
    
    idPaciente: int | None = None #este si es necesario, pero se puede llenar con la sesión del usuario despues

    #relaciones no necesarias
    idRecepcionista: int | None = None
    idMedico: int | None = None

    #Lista de sintomas
    Sintomas: List[Cita_SintomaCreate] = []

class Cita(_CitaBase):
    idCita: int
    idFecha: int #con esto se puede obtener la fecha
    idPaciente: int
    Sintomas: List[Cita_Sintoma] = []
    #datos opcionales
    idRecepcionista: int | None = None
    idMedico: int | None = None
    #opcionalmente podemos mandar la fecha directamente, haciendo una consulta desde el BackEnd
    fecha: datetime | None = None

    model_config = {"from_attributes": True}