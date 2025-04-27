from pydantic import BaseModel

class _Cita_SintomaBase(BaseModel):
    sintoma: str

class Cita_SintomaCreate(_Cita_SintomaBase):
    idCita: int


class Cita_Sintoma(_Cita_SintomaBase):
    idSintoma: int
    idCita: int

    model_config = {"from_attributes": True}
