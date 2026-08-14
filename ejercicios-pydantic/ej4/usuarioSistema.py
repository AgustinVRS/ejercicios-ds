"""
Escribir un bloque de código que intente instanciar un modelo
UsuarioSistema con campos:
● email: utilizar EmailStr
● nivel_acceso: entero entre 1 y 5
proveyendo datos incorrectos.
Capturar explícitamente la excepción ValidationError
imprimiendo por pantalla los errores detallados. (Ver:
try/except)
"""
from pydantic import BaseModel,EmailStr,Field, ValidationError
from typing import Annotated

class UsuarioSistema(BaseModel):
    email: EmailStr
    nivel_acceso: Annotated[int,Field(ge=1,le=5)]


if __name__ == "__main__":

    try:
        e1= UsuarioSistema(email="agustin@ejemplo.com", nivel_acceso=10)
    except ValidationError as e:
        print("\nError de Validacion: ",e)

    try:
        e1= UsuarioSistema(email=1, nivel_acceso=2)
    except ValidationError as e:
        print("\nError de Validacion: ",e)