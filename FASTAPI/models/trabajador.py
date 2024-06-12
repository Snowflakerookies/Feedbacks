from pydantic import BaseModel
from typing import Optional

# Definición del modelo de datos para un trabajador
class Trabajador(BaseModel):
    NOMBRE: str
    APELLIDO1: str
    APELLIDO2: Optional[str] = None
    EMAIL: str
    VERTICAL: str
    COHORTE : str
    PUESTO: str
