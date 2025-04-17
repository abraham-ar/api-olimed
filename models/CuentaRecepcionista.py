from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped
from config.db import Base
import passlib.hash as _hash

class CuentaRecepcionista(Base):
    __tablename__ = "CuentaRecepcionista"

    idRecepcionista: Mapped[int] = mapped_column(primary_key=True)
    clave: Mapped[str] = mapped_column(String(45), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    correo: Mapped[str] = mapped_column(String(100), unique=True)
    telefono: Mapped[str] = mapped_column(String(20))

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)