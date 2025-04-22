from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from config.db import Base
import passlib.hash as _hash
from typing import List
from models import Cita

class CuentaRecepcionista(Base):
    __tablename__ = "CuentaRecepcionista"

    idRecepcionista: Mapped[int] = mapped_column(primary_key=True)
    clave: Mapped[str] = mapped_column(String(45), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    correo: Mapped[str] = mapped_column(String(100), unique=True)
    telefono: Mapped[str] = mapped_column(String(20))

    #Citas creadas por el recepcionista
    Citas: Mapped[List["Cita"]] = relationship(back_populates="Recepcionista")

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)