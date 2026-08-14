"""
Crear un tipo reutilizable CoordenadaGPS con Annotated que
sea un float entre -90.0 y 90.0.
Luego, implementa un modelo Ubicacion que use este tipo
de dato para sus atributos: longitud y latitud y que además
tenga un atributo opcional etiqueta (string).
Crear una instancia de este modelo para comprobar el uso del
tipo reutilizable, mostrando por pantalla lo que tenga la
instancia.
Crear otra instancia para comprobar el error de validación al
utilizar valores inválidos de latitud/longitud.
"""

from pydantic import BaseModel,Field,ValidationError
from typing import Annotated,Optional

CoordenadasGPS = Annotated[float,Field(ge=-90.00,le=90.00)]

class Ubicacion(BaseModel):
    longitud: CoordenadasGPS
    latitud: CoordenadasGPS
    etiqueta: Optional[str] = None

if __name__ == "__main__":

    u1 = Ubicacion(longitud=33.3,latitud=-33.3)
    print("Ubicacion creada correctamente:")
    print(u1)

#   ---- Casos Invalidos ----   
    try:
        u2 = Ubicacion(longitud=100.0,latitud=-33.3)
        print("Ubicacion creada correctamente:")
        print(u2, "\n")
    except ValidationError as e:
        print("\nError inesperado: ", e)

    try:
        u3 = Ubicacion(longitud=33.3,latitud=-100)
        print("Ubicacion creada correctamente:")
        print(u3, "\n")
    except ValidationError as e:
        print("\nError inesperado: ", e)       