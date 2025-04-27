from pydantic import BaseModel, SecretStr

class AdminLogin(BaseModel):
    clave: int
    password: SecretStr