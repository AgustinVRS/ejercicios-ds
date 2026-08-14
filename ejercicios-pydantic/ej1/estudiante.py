"""
Crear un modelo Estudiante que contenga:
● legajo: entero positivo
● nombre_completo: string de al menos 5 caracteres
● email: string con formato de correo electrónico
● promedio: float entre 0.0 y 10.0 con valor por defecto de 0.0
Crear una instancia por cada posible error de validación para
observar el mensaje que nos da Python al utilizar valores
inválidos. 
"""

from typing import Annotated
from pydantic import BaseModel, EmailStr, Field, ValidationError

class Estudiante(BaseModel):
    legajo: Annotated[int, Field(gt=0, description="Debe ser mayor a 0")]
    nombre_completo: Annotated[str, Field(min_length=5, description="Mínimo 5 caracteres")]
    email: EmailStr
    promedio: Annotated[float, Field(ge=0.0, le=10.0, description="Rango de 0.0 a 10.0")] = 0.0

if __name__ == "__main__":

    try:
        e1 = Estudiante(legajo=1,nombre_completo="Agustin Vargas",email="agustin@ejemplo.com",promedio=9.5)
        print("Estudiante creado correctamente:")
        print(e1, "\n")
    except ValidationError as e:
        print("Error inesperado: ", e)

    #---- Casos Invalidos ----
    
        e2 = Estudiante(legajo=-1,nombre_completo="El Tobi",email="tobi@ejemplo.com")
        print("Estudiante creado correctamente:")
        print(e2, "\n")

        e3 = Estudiante(legajo=2,nombre_completo=1000,email="tobi@ejemplo.com")
        print("Estudiante creado correctamente:")
        print(e3, "\n")

"""
    try:
        e3 = Estudiante(legajo=2,nombre_completo=1000,email="tobi@ejemplo.com")
        print("Estudiante creado correctamente:")
        print(e3, "\n")
    except ValidationError as e:
        print("\nError inesperado: ",e)

    try:
        e4 = Estudiante(legajo=3,nombre_completo="Facundo",email=1)
        print("Estudiante creado correctamente:")
        print(e4, "\n")
    except ValidationError as e:
        print("\nError inesperado: ",e)

    try:
        e3 = Estudiante(legajo=4,nombre_completo="Agustin Vargas",email="agustin@ejemplo.com",promedio=100.0)
        print("Estudiante creado correctamente:")
        print(e3, "\n")
    except ValidationError as e:
        print("\nError inesperado: ",e)

""" 