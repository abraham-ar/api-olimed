from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from config.db import engine, Base
import passlib.hash as _hash
from typing import Optional
from datetime import date

class CuentaPaciente(Base):
    __tablename__ = "CuentaPaciente"
    
    idPaciente: Mapped[int] = mapped_column(primary_key=True)

    #datos de inicio de sesion
    correo : Mapped[str]= mapped_column(String(100), unique=True, nullable=False)
    hashed_password : Mapped[str] = mapped_column(String(100), nullable=False)

    #datos de contacto
    nombre : Mapped[str] = mapped_column(String(100), nullable=False)
    direccion : Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    telefono : Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    #datos medicos
    tipo_sangre : Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    alergias : Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    fecha_nacimiento : Mapped[date] = mapped_column(nullable=True)

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)