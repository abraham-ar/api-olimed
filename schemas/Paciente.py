from pydantic import BaseModel, EmailStr, SecretStr
from datetime import date

class _PacienteBase(BaseModel):
    #datos generales
    correo: EmailStr
    nombre: str

class PacienteCreate(_PacienteBase): #datos de registro
    password: SecretStr 
    fecha_nacimiento: date

class Paciente(_PacienteBase):
    idPaciente: int
    tipo_sangre: str | None = None
    alergias: str | None = None
    direccion: str | None = None
    telefono: str | None = None
    class Config:
        orm_mode = True
        

class PacienteForRecepcionista(_PacienteBase): #datos de contacto y id
    idPaciente: int

    class Config:
        orm_mode = True
    
class PacienteRecoverPassword(_PacienteBase): #recuperar contraseña
    new_password: SecretStr

class PacienteUpdatePassword(BaseModel): #actualización de password
    current_password: SecretStr
    new_password: SecretStr