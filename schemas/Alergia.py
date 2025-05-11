from pydantic import BaseModel

class _AlergiaBase(BaseModel):
    nombre: str

class AlergiaUpdate(BaseModel):
    nombre: str | None = None

#usado cuando se registra una nueva alergia
class AlergiaCreate(BaseModel):
    nombre: str

class Alergia(_AlergiaBase):
    id: int
    idPaciente: int

    model_config = {"from_attributes": True}