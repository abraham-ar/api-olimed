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
    Alergias: List[Alergia] = []
    direccion: str | None = None
    fecha_nacimiento: date
    Telefonos: List[Paciente_Telefono] = []

    model_config = {"from_attributes": True}
        

class PacienteUpdate(BaseModel):
    nombre: str | None = None
    fecha_nacimiento: date | None = None
    tipo_sangre: str | None =  None
    direccion: str | None = None

class PacienteForRecepcionista(_PacienteBase): #datos de contacto y id
    idPaciente: int

    model_config = {"from_attributes": True}

class PacienteRecoverPassword(_PacienteBase): #recuperar contraseña
    new_password: SecretStr

class PacienteUpdatePassword(BaseModel): #actualización de password
    current_password: SecretStr
    new_password: SecretStr