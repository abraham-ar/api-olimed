from pydantic import BaseModel, EmailStr, SecretStr

class _PacienteBase(BaseModel):
    #datos generales
    correo: EmailStr
    nombre: str
    direccion: str

class PacienteCreate(_PacienteBase): #datos de registro
    hashed_password: str #ppsiblemente no sea la hashed, solo password 
    tipo_sangre: str | None = None
    alergias: str | None = None

    
class Paciente(_PacienteBase):
    idPaciente: int
    tipo_sangre: str | None = None
    alergias: str | None = None

    class Config:
        orm_mode = True
        

class PacienteForRecepcionista(_PacienteBase): #datos de contacto y id
    idPaciente: int

    class Config:
        orm_mode = True
    
class PacienteUpdatePassword(BaseModel): #actualización de password
    current_password: str
    new_password: str