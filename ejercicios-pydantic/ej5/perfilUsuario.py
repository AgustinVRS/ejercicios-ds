"""
Construir un modelo PerfilUsuario que combine:
● username: string alfanumérico en minúsculas usando el
atributo pattern de Field y la expresión regular
r"^[a-z0-9_]{3,20}$"
● biografia: opcional, con un máximo de 200 caracteres.
● redes_sociales: lista opcional de strings, URLs o
nombres. (Ver Types/urls)
"""
from pydantic import BaseModel,Field,HttpUrl
from typing import Annotated, Optional,Union

class PerfilUsuario(BaseModel):
    username: Annotated[str,Field(pattern=r"^[a-z0-9_]{3,20}$")]
    biografia: Optional[str] = Field(default=None, max_length=200)
    redes_sociales: Optional[list[Union[HttpUrl, str]]] = None

if __name__ == "__main__":

    p1 = PerfilUsuario(username="agustin_v",redes_sociales=["https://github.com/AgustinVRS", "@agustinv"])
    print(p1)