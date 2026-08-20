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
from sqlalchemy import String, ForeignKey, DateTime, select,Float
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

    cursos: Mapped[list["Curso"]] = relationship(back_populates="profesor")

class Curso(Base):

    __tablename__ = "cursos"

    id: Mapped[int] = mapped_column(primary_key=True)    
    titulo: Mapped[str] = mapped_column(String(100))
    creditos: Mapped[float] = mapped_column(Float)

    profesor_id: Mapped[int] = mapped_column(ForeignKey("profesores.id"))
    profesor: Mapped["Profesor"] = relationship (back_populates="cursos")

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":

    with Session(engine) as session:
        depto_matematicas = Departamento(
            nombre="Matematicas",
            profesores=[
                Profesor(nombre="Carlos Ruiz", email="carlosruiz@unp.edu.ar",
                cursos=[Curso(titulo="Álgebra Lineal", creditos=5.5), Curso(titulo="Análisis Matemático", creditos=6.0)]),                    
                Profesor(nombre="Agustin Vargas", email ="agustinvargas@unp.edu.ar",
                cursos=[Curso(titulo="Estadística", creditos=4.0)])])

        session.add(depto_matematicas)
        session.commit()
        print("-> Departamentps, Profesores, Cursos Guardados Correctamente\n")

        stmt_prof = select(Profesor).where(Profesor.email == "agustinvargas@unp.edu.ar")
        prof = session.scalars(stmt_prof).first()

        if prof:
            print(f"Profesor: {prof.nombre}")
            print("Cursos que dicta:")
            for curso in prof.cursos:
                print(f"   -  {curso.titulo} ({curso.creditos} créditos)")
        stmt_curso = select(Curso).where(Curso.titulo == "Estadística")
        curso = session.scalars(stmt_curso).first()

        if curso:
            print(f"   Curso: {curso.titulo} ({curso.creditos} créditos)")
            print(f"   Dictado por: {curso.profesor.nombre}")
            print(f"   Área: {curso.profesor.departamento.nombre}")