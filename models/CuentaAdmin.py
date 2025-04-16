from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column
from config.db import Base
import passlib.hash as _hash

class CuentaAdmin(Base):
    __tablename__ = "CuentaAdmin"

    idAdmin = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre = mapped_column(String(100), nullable=False)
    clave = mapped_column(String(45), unique=True)
    hashed_password = mapped_column(String(100), nullable=False)

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)