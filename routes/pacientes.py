from fastapi import APIRouter

pacientes = APIRouter()

@pacientes.get("/pacientes")
def getPacientes():
    return "hola FastAPI"

@pacientes.post("/pacientes/")
def getPaciente(id_paciente: int):
    return {"nombre": str(id_paciente)}

@pacientes.get("/paciente/{id_paciente}")
def getPaciente(id_paciente: int):
    return {"nombre": str(id_paciente)}

@pacientes.put("/paciente/{id_paciente}")
def getPaciente(id_paciente: int):
    return {"nombre": str(id_paciente)}

@pacientes.delete("/paciente/{id_paciente}")
def getPaciente(id_paciente: int):
    return {"nombre": str(id_paciente)}