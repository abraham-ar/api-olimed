from pydantic import BaseModel

class _RecetaBase(BaseModel):
    tratamiento: str

