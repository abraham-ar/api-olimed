from sqlalchemy import Table, Column, Integer, String, DATE
from sqlalchemy.orm import mapped_column
from config.db import engine, Base
import passlib.hash as _hash

class CuentaPaciente(Base):
    __tablename__ = "CuentaPaciente"
    
    idPaciente = mapped_column(Integer, primary_key=True, autoincrement=True)

    #datos de inicio de sesion
    correo = mapped_column(String(100), unique=True)
    hashed_password = mapped_column(String(100), nullable=False)

    #datos de contacto
    nombre = mapped_column(String(100), nullable=False)
    direccion = mapped_column(String(100), nullable=False)
    telefono = mapped_column(String(20), nullable=False)

    #datos medicos
    tipo_sangre = mapped_column(String(30), nullable=True)
    alergias = mapped_column(String(200), nullable=True)
    fecha_nacimiento = mapped_column(DATE, nullable=True)

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)