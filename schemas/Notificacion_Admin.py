from pydantic import BaseModel, Field
from datetime import datetime

class _Notificacion_AdminBase(BaseModel):
    titulo: str
    mensaje: str
    tipo: str

class Notificacion_AdminCreate(_Notificacion_AdminBase):
    idAdmin: int | None = None
    fecha_creacion: datetime = Field(default_factory=datetime.now)

class Notificacion_Admin(_Notificacion_AdminBase):
    idNotificacion: int
    idAdmin: int
    fecha_creacion: datetime

    class Config: 
        orm_mode = True
