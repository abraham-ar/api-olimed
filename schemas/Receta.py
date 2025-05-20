from pydantic import BaseModel, Field
from datetime import datetime

class _RecetaBase(BaseModel):
    tratamiento: str
    #campos opcionales a continuación
    talla: int | None = None
    peso: float | None = None
    fc: int | None = None
    fr: int | None = None
    saturacion_oxigeno: str | None = None
    presion_arterial: str | None = None
    temperatura: float | None = None

class RecetaUpdate(BaseModel):
    tratamiento: str | None = None
    talla: int | None = None
    peso: float | None = None
    fc: int | None = None
    fr: int | None = None
    saturacion_oxigeno: str | None = None
    presion_arterial: str | None = None
    temperatura: float | None = None

class RecetaCreate(_RecetaBase):
    idCita: int
    fecha_creacion: datetime = Field(default_factory=datetime.now)    

class Receta(_RecetaBase):
    #idReceta: int
    idCita: int
    fecha_creacion: datetime

    model_config = {"from_attributes": True}