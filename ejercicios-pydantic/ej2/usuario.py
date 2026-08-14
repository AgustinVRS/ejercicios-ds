"""
Crear un modelo Dispositivo que contenga:
● id_dispositivo: puede ser un entero o una cadena
● tipo: Literal que solo acepte los valores “sensor”,
“actuador” o “gateway”.
Crear una instancia de este modelo para comprobar el uso del
atributo id_dispositivo como Union de dos tipos de datos y
otra instancia para comprobar el error de validación al utilizar
valores inválidos.
"""
from pydantic import BaseModel,ValidationError
from typing import Union, Literal

class Dispositivo(BaseModel):
    id_dispositivo: Union[int,str]
    tipo: Literal["sensor","actuador","gateway"]

if __name__ == "__main__":

    d1 = Dispositivo(id_dispositivo="1",tipo="sensor")
    print("Se Creo un Nuevo disposistivo\n",d1)

try:
    d2 = Dispositivo(id_dispositivo=1.0,tipo="sensor")
    print("Se Creo un Nuevo disposistivo\n",d2)
except ValidationError as e:
    print("\nError de Validacion: ",e)  