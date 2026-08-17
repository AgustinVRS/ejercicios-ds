"""
Crear el archivo de configuración de la base de datos (puede ser
SQLite en memoria o archivo) y definir el primer modelo
Profesor con los campos: id, nombre, email y fecha_ingreso
(Ver DateTime).
Insertar un par de registros de prueba y mostrarlos por consola.
"""

from datetime import datetime
from database import Base, engine
from sqlalchemy import DateTime, String, select
from sqlalchemy.orm import Mapped, Session, mapped_column

class Profesor(Base):
    __tablename__ = "profesores"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    fecha_ingreso: Mapped[datetime] = mapped_column(DateTime)

    def __repr__(self) -> str:
        return f"<Profesor(id={self.id}, nombre='{self.nombre}', email='{self.email}')>"


Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    with Session(engine) as session:
        prof1 = Profesor(
            nombre="Carlos Benitez",
            email="carlos.benitez@unp.edu.ar",
            fecha_ingreso=datetime(2021, 3, 15, 8, 30),
        )
        prof2 = Profesor(
            nombre="Mariana Gomez",
            email="mariana.gomez@unp.edu.ar",
            fecha_ingreso=datetime.now(),
        )

        session.add(prof1)
        session.add(prof2)
        session.commit()

        stmt = select(Profesor)
        profesores = session.scalars(stmt).all()

        for prof in profesores:
            print(prof)