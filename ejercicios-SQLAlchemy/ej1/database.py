from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Configuración del motor de conexión (Engine)
engine = create_engine("sqlite://", echo=True)