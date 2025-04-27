from pydantic import BaseModel

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

class RecetaCreate(_RecetaBase):
    idCita: int    

class Receta(_RecetaBase):
    idReceta: int
    idCita: int

    model_config = {"from_attributes": True}