from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from config.db import Base
from datetime import datetime
#from models import Cita
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Cita

class Receta(Base):
    __tablename__ = "Receta"

    #la clave foranea actua tambien como clave primaria
    idCita: Mapped[int] = mapped_column(ForeignKey("Cita.idCita"), primary_key=True)

    #campos opcionales
    talla: Mapped[Optional[int]] = mapped_column(nullable=True)
    peso: Mapped[Optional[float]] = mapped_column(nullable=True)
    fc: Mapped[Optional[int]] = mapped_column(nullable=True)
    fr: Mapped[Optional[int]] = mapped_column(nullable=True)
    saturacion_oxigeno: Mapped[Optional[str]] = mapped_column(String(10) ,nullable=True)
    presion_arterial: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    temperatura: Mapped[Optional[float]] = mapped_column(nullable=True)

    #nuevo campo obligatorio
    fecha_creacion: Mapped[datetime] = mapped_column(nullable=False ,default=datetime.now())

    #obligatorio
    tratamiento: Mapped[str] = mapped_column(String(500), nullable=False)

    #relacion modelada con ORM
    Cita: Mapped["Cita"] = relationship(back_populates="Receta", single_parent=True)




