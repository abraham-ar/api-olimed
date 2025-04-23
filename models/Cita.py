from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from datetime import datetime
from models import CuentaPaciente
from config.db import Base
from models import CuentaAdmin, CuentaPaciente, CuentaRecepcionista, Cita_Sintoma, Receta, FechaDisponible

class Cita(Base):
    __tablename__ = "Cita"

    idCita: Mapped[int] = mapped_column(primary_key=True)

    #relacion principal, depende del paciente para quien es la cita
    idPaciente: Mapped[int] = mapped_column(ForeignKey("CuentaPaciente.idPaciente") ,nullable=False)

    #relación con la FechaDisponible
    idFecha: Mapped[int] = mapped_column(ForeignKey("FechaDisponible.idFecha"), nullable=False)

    #relacion opcional, solo si quien crea la cita es medico o recepcionista
    idMedico: Mapped[Optional[int]] = mapped_column(ForeignKey("CuentaAdmin.idAdmin"), nullable=True)
    idRecepcionista: Mapped[Optional[int]] = mapped_column(ForeignKey("CuentaRecepcionista.idRecepcionista"), nullable=True)

    #información general de la cita
    #fecha: Mapped[datetime] = mapped_column(nullable=False) ESTO SE OBTIENE DE SU RELACION CON FECHADISPONIBLEs
    estado: Mapped[int] = mapped_column(nullable=False)
    #relacion con Cita_Sintoma
    Sintomas: Mapped[List["Cita_Sintoma"]] = relationship(back_populates="Cita", cascade="all, delete-orphan")

    #campos que permiten realizar operaciones JOIN usando ORM
    Paciente: Mapped["CuentaPaciente"] = relationship(back_populates="Citas")
    Fecha: Mapped["FechaDisponible"] = relationship(back_populates="Cita")
    Receta: Mapped[Optional["Receta"]] = relationship(back_populates="Cita", cascade="all, delete-orphan")

    #campos de relación ORM opcionales
    Medico: Mapped[Optional["CuentaAdmin"]] = relationship(back_populates="Citas")
    Recepcionista: Mapped[Optional["CuentaRecepcionista"]] = relationship(back_populates="Citas")
    