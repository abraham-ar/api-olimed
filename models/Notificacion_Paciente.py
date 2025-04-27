from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from datetime import datetime
from config.db import Base
#from models import CuentaPaciente
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import CuentaPaciente


class Notificacion_Paciente(Base):
    __tablename__ = "Notificacion_Paciente"

    idNotificacion: Mapped[int] = mapped_column(primary_key=True)
    idPaciente: Mapped[int] = mapped_column(ForeignKey("CuentaPaciente.idPaciente"), nullable=False)

    tipoNotificacion: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    titulo: Mapped[str] = mapped_column(String(45), nullable=False)
    mensaje: Mapped[str] = mapped_column(String(150), nullable=False)
    fecha_creacion: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    Paciente: Mapped["CuentaPaciente"] = relationship(back_populates="Notificaciones")