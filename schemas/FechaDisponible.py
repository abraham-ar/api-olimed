from pydantic import BaseModel
from datetime import datetime

class _FechaDisponibleBase(BaseModel):
    fecha: datetime
    disponible: int

class FechaDisponibleCreate(_FechaDisponibleBase):
    idAdmin: int | None = None
    seleccionado: str | None = None

class FechaDisponible(_FechaDisponibleBase):
    idFecha: int
    idAdmin: int | None = None
    seleccionado: str | None = None

    model_config = {"from_attributes": True}