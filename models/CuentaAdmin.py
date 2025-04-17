from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from config.db import Base
import passlib.hash as _hash
  
class CuentaAdmin(Base):
    __tablename__ = "CuentaAdmin"

    idAdmin : Mapped[int] = mapped_column(primary_key=True)
    nombre : Mapped[str] = mapped_column(String(100), nullable=False)
    clave : Mapped[str] = mapped_column(String(45), unique=True, nullable=False)
    hashed_password : Mapped[str] = mapped_column(String(100), nullable=False)

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)