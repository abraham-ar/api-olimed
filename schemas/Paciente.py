from pydantic import BaseModel, EmailStr, SecretStr
from datetime import date
from typing import List
from .Alergia import Alergia
from .Paciente_Telefono import Paciente_Telefono


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
    alergias: List[Alergia] = []
    direccion: str | None = None
    telefonos: List[Paciente_Telefono] = []

    model_config = {"from_attributes": True}
        

class PacienteForRecepcionista(_PacienteBase): #datos de contacto y id
    idPaciente: int

    model_config = {"from_attributes": True}

class PacienteLogin(BaseModel):
    correo: EmailStr
    password: str
    
class PacienteRecoverPassword(_PacienteBase): #recuperar contraseña
    new_password: SecretStr

class PacienteUpdatePassword(BaseModel): #actualización de password
    current_password: SecretStr
    new_password: SecretStr