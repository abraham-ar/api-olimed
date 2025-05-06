from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from config.db import Base
from typing import Optional
#from models import CuentaAdmin, Cita
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import CuentaAdmin, Cita

class FechaDisponible(Base):
    __tablename__ = "FechaDisponible"

    idFecha: Mapped[int] = mapped_column(primary_key=True)

    #Clave foranea, define el medico que atiende (considerando que el sistema admita mas medicos en el futuro)
    idAdmin: Mapped[Optional[int]] = mapped_column(ForeignKey("CuentaAdmin.idAdmin"), nullable=True) 

    fecha: Mapped[datetime] = mapped_column(nullable=False)
    disponible: Mapped[int] = mapped_column(nullable=False)

    seleccionado: Mapped[Optional[int]] = mapped_column(nullable=True)

    #relacion usada para el ORM
    Medico: Mapped["CuentaAdmin"] = relationship(back_populates="Fechas")
    Cita: Mapped["Cita"] = relationship(back_populates="Fecha", cascade="all, delete-orphan")