from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models import CuentaAdmin
from config.db import Base
#from models import CuentaAdmin
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import CuentaAdmin


class Notificacion_Admin(Base):
    __tablename__ = "Notificacion_Admin"

    idNotificacion: Mapped[int] = mapped_column(primary_key=True)

    #clave foranea de CuentaAdmin
    idAdmin: Mapped[int] = mapped_column(ForeignKey("CuentaAdmin.idAdmin"), nullable=False)

    tipo: Mapped[str] = mapped_column(String(45), nullable=False)
    titulo: Mapped[str] = mapped_column(String(45), nullable=False)
    mensaje: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha_creacion: Mapped[datetime] = mapped_column(nullable=False)

    Admin: Mapped["CuentaAdmin"] = relationship(back_populates="Notificaciones")