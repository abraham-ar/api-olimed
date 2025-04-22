from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from config.db import Base
from models import CuentaPaciente

class Paciente_Telefono(Base):

    __tablename__ = "Paciente_Telefono"

    id: Mapped[int] = mapped_column(primary_key=True)
    idPaciente: Mapped[int] = mapped_column(ForeignKey("CuentaPaciente.idPaciente"), nullable=False)

    telefono: Mapped[str] = mapped_column(String(20), nullable=False)
    tipo: Mapped[str] = mapped_column(String(10), nullable=False)

    Paciente: Mapped["CuentaPaciente"] = relationship(back_populates="Telefonos")