from pydantic import BaseModel

class _AlergiaBase(BaseModel):
    nombre: str

#usado cuando se registra una nueva alergia
class AlergiaCreate(_AlergiaBase):
    idPaciente: int | None = None

class Alergia(_AlergiaBase):
    id: int
    idPaciente: int

    model_config = {"from_attributes": True}