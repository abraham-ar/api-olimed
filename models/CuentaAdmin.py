from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from config.db import Base
import passlib.hash as _hash
from typing import List
from models import Cita, Notificacion_Admin, FechaDisponible
  
class CuentaAdmin(Base):
    __tablename__ = "CuentaAdmin"

    idAdmin : Mapped[int] = mapped_column(primary_key=True)
    nombre : Mapped[str] = mapped_column(String(100), nullable=False)
    clave : Mapped[str] = mapped_column(String(45), unique=True, nullable=False)
    hashed_password : Mapped[str] = mapped_column(String(100), nullable=False)

    #notificaciones del Admin
    Notificaciones: Mapped[List["Notificacion_Admin"]] = relationship(back_populates="Admin", cascade="all delete-orphan")

    #relacion con Cita, citas creadas por el medico
    Citas: Mapped[List["Cita"]] = relationship(back_populates="Medico")

    #relacion con FechasDisponibles
    Fechas: Mapped["FechaDisponible"] = relationship(back_populates="Medico", cascade="all, delete-orphan")

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)