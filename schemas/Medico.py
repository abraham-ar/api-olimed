from pydantic import BaseModel, SecretStr

class _MedicoBase(BaseModel):
    #datos generales
    nombre: str

class MedicoCreate(_MedicoBase): #datos de registro
    password: SecretStr

class Medico(_MedicoBase):
    idAdmin: int
    clave: str

    model_config = {"from_attributes": True}
        
class MedicoUpdatePassword(BaseModel): #actualización de password
    current_password: str
    new_password: str