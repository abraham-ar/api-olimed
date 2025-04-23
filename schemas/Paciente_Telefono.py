from pydantic import BaseModel

class _Paciente_TelefonoBase(BaseModel):
    telefono: str
    tipo: str

class Paciente_TelefonoCreate(_Paciente_TelefonoBase):
    idPaciente: int | None = None

class Paciente_Telefono(_Paciente_TelefonoBase):
    id: int
    idPaciente: int

    class Config:
        orm_mode = True