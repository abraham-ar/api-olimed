from config.db import Base, engine
from models import CuentaAdmin, CuentaRecepcionista, CuentaPaciente, Alergia , Paciente_Telefono, Notificacion_Paciente, Cita, Cita_Sintoma, Receta, FechaDisponible, Notificacion_Admin

def create_database():
    return Base.metadata.create_all(bind=engine)
