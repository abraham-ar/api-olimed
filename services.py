from config.db import Base, engine
from models import CuentaAdmin, CuentaRecepcionista, CuentaPaciente

def create_database():
    return Base.metadata.create_all(bind=engine)
