"""
1. Crear un nuevo modelo Departamento (id, nombre).
2. Modificar el modelo Profesor para agregarle una clave
foránea departamento_id.
3. Utilizar relationship en el modelo Departamento para
acceder a la lista de sus profesores.
Insertar un par de registros de prueba y mostrarlos por consola.
"""

from datetime import datetime
from database import Base, engine
from sqlalchemy import String, ForeignKey, DateTime, select
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

class Departamento(Base):

    __tablename__ = "departamentos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))

    profesores: Mapped[list["Profesor"]] = relationship(back_populates="departamento")

class Profesor(Base):
    
    __tablename__ = "profesores"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    fecha_ingreso: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    departamento_id: Mapped[int] = mapped_column(ForeignKey("departamentos.id"))
    departamento: Mapped["Departamento"] = relationship(back_populates="profesores")

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":

    with Session(engine) as session:
        depto_sistemas = Departamento(
            nombre="Sistemas",
            profesores=[
                Profesor(nombre="Carlos Ruiz", email="carlosruiz@unp.edu.ar"),
                Profesor(nombre="Lucía Gómez", email="luciagomez@unp.edu.ar")
                ]
            )
        depto_matematicas = Departamento(
            nombre = "Matematicas",
            profesores= [Profesor(nombre="Agustin Vargas", email ="agustinvargas@unp.edu.ar")]  
            )

        session.add(depto_sistemas)
        session.add(depto_matematicas)
        session.commit()
        print("-> Departamento y Profesores guardados exitosamente.\n")

        stmt = select(Departamento)
        deptos = session.scalars(stmt).all()
        
        for depto in deptos:
            print(f"Departamento: {depto.nombre}")
            print("Lista de profesores (obtenida mediante la relación):")
            for prof in depto.profesores:
                print(f" - {prof.nombre} | {prof.email}")
                    
