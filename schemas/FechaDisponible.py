from pydantic import BaseModel
from datetime import datetime

class _FechaDisponibleBase(BaseModel):
    fecha: datetime
    disponible: int

class FechaDisponibleCreate(_FechaDisponibleBase):
    idAdmin: int | None = None
    seleccionado: int | None = None

class FechaDisponibleUpdate(BaseModel):
    fecha: datetime | None = None
    disponible: int | None = None
    idAdmin: int | None = None
    seleccionado: int | None = None


class FechaDisponible(BaseModel):
    idFecha: int
    fecha: datetime
    disponible: int | None = None

    model_config = {"from_attributes": True}