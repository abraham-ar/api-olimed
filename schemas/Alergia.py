from pydantic import BaseModel, EmailStr, SecretStr
from datetime import date

class _AlergiaBase(BaseModel):
    nombre: str

#usado cuando se registra una nueva alergia
class AlergiaCreate(_AlergiaBase):
    idPaciente: int | None = None

class Alergia(_AlergiaBase):
    id: int
    idPaciente: int

    class Config:
        orm_mode = True