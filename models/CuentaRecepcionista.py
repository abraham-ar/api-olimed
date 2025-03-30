from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column
from config.db import Base
import passlib.hash as _hash

class CuentaRecepcionista(Base):
    __tablename__ = "CuentaRecepcionista"

    idRecepcionista = mapped_column(Integer, primary_key=True, autoincrement=True)
    clave = mapped_column(String(45), unique=True, nullable=False)
    hashed_password = mapped_column(String(100), nullable=False)
    nombre = mapped_column(String(100), nullable=False)
    correo = mapped_column(String(100), unique=True)
    telefono = mapped_column(String(20))

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)