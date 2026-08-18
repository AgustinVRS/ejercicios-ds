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
            nombre="Matematicas",
            profesores=[
                Profesor(nombre="Carlos Ruiz", email="carlosruiz@unp.edu.ar"),
                Profesor(nombre="Lucía Gómez", email="luciagomez@unp.edu.ar"),
                Profesor(nombre="Agustin Vargas", email ="agustinvargas@unp.edu.ar")]
            )

        session.add(depto_sistemas)
        session.commit()
        print("-> Departamento y 3 Profesores guardados exitosamente.\n")

        stmt_depto = select(Departamento).where(Departamento.nombre == "Matematicas")
        depto = session.scalars(stmt_depto).first()

        if depto:
            print(f"Departamento: {depto.nombre}")
            print(f"Lista Profesores (depto.profesores):")
            for prof in depto.profesores:
                print(f" - {prof.nombre} | {prof.email}")

        stmt_profe = select(Profesor).where(Profesor.email == "agustinvargas@unp.edu.ar")
        prof_elegido = session.scalars(stmt_profe).first()

        if prof_elegido:
            print(f"Profesor Consultado: {prof_elegido.nombre} ")
            print(f"Pertenece al Departamento: {prof_elegido.departamento.nombre}")