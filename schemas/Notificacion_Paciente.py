from pydantic import BaseModel, Field
from datetime import datetime

class _Notificacion_PacienteBase(BaseModel):
    titulo: str
    mensaje: str

class Notificacion_PacienteCreate(_Notificacion_PacienteBase):
    idPaciente: int
    tipoNotificacion: str | None = None
    fecnaCreacion: datetime = Field(default_factory=datetime.now)

class Notificacion_Paciente(_Notificacion_PacienteBase):
    idNotificacion: int
    idPaciente: int
    tipoNotificacion: str | None = None
    fechaCreacion: datetime

    model_config = {"from_attributes": True}