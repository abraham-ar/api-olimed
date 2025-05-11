from pydantic import BaseModel

class _Paciente_TelefonoBase(BaseModel):
    telefono: str
    tipo: str

class Paciente_TelefonoCreate(_Paciente_TelefonoBase):
    pass

class Paciente_TelefonoUpdate(BaseModel):
    telefono: str | None = None
    tipo: str | None = None

class Paciente_Telefono(_Paciente_TelefonoBase):
    id: int
    idPaciente: int

    model_config = {"from_attributes": True}