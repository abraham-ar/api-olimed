from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from config.db import Base
from models import Cita

class Cita_Sintoma(Base):
    __tablename__= "Cita_Sintoma"

    idSintoma: Mapped[int] = mapped_column(primary_key=True)

    idCita: Mapped[int] = mapped_column(ForeignKey("Cita.idCita"), nullable=False)
    
    sintoma: Mapped[str] = mapped_column(String(100), nullable=False)

    Cita: Mapped["Cita"] = relationship(back_populates="Sintomas")