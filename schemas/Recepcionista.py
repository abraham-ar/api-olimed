from pydantic import BaseModel, EmailStr, SecretStr

class _RecepcionistaBase(BaseModel):
    #datos generales
    nombre: str

class RecepcionistaCreate(_RecepcionistaBase): #datos de registro
    correo: EmailStr
    telefono: str
    password: SecretStr

class RecepcionistaSimple(_RecepcionistaBase):
    clave: str

    class Config:
        orm_mode = True

class Recepcionista(_RecepcionistaBase):
    idRecepcionista: int
    clave: str

    class Config:
        orm_mode = True
        
class RecepcionistaRecoverPassword(_RecepcionistaBase):
    correo: EmailStr
    new_password: SecretStr

class RecepcionistaUpdatePassword(BaseModel): #actualización de password
    current_password: SecretStr
    new_password: SecretStr