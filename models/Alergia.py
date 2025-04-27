from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
#from models import CuentaPaciente
from config.db import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import CuentaPaciente


class Alergia(Base):
    __tablename__ = "Alergia"

    id: Mapped[int] = mapped_column(primary_key=True)

    #relación con CuentaPaciente
    idPaciente: Mapped[int] = mapped_column(ForeignKey("CuentaPaciente.idPaciente"), nullable=False)

    nombre: Mapped[str] = mapped_column(String(45), nullable=False)

    Paciente: Mapped["CuentaPaciente"] = relationship(back_populates="Alergias")