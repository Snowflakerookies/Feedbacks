from pydantic import BaseModel

class Trabajador(BaseModel):
    NOMBRE: str
    APELLIDO1: str
    APELLIDO2: str
    PUESTO: str
    EMAIL: str
    VERTICAL: str
