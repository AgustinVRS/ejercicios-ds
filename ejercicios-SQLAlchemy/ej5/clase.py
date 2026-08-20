"""
Crea el modelo Clase (id, tema, duracion_minutos).
Un curso se compone de muchas clases.
Configurar la relación One-to-Many entre Curso y Clase.
Escribir una consulta que devuelva todas las clases de un curso
específico a través del ORM.
"""

from datetime import datetime
from database import Base, engine
from sqlalchemy import String, ForeignKey, DateTime, select,Float,Integer
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

    clases: Mapped[list["Clase"]] = relationship(back_populates="cursos")

class Clase(Base):

    __tablename__ = "clases"

    id: Mapped[int] = mapped_column(primary_key=True)
    tema: Mapped[str] = mapped_column(String(50))
    duracion_minutos: Mapped[int] = mapped_column(Integer)

    curso_id: Mapped[int] = mapped_column(ForeignKey("cursos.id"))
    cursos: Mapped["Curso"] = relationship(back_populates="clases")

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":

    with Session(engine) as session:

        depto = Departamento(nombre="Ciencias Exactas",
                profesores=[Profesor(nombre="Agustin Vargas", email="agustin.vargas@unp.edu.ar",
                cursos=[Curso(titulo="Álgebra Lineal", creditos=5.0,
                clases=[Clase(tema="Matrices y Determinantes", duracion_minutos=90,),
                        Clase(tema="Espacios Vectoriales", duracion_minutos=120,),
                        Clase(tema="Transformaciones Lineales", duracion_minutos=90,)])])
                        ]
                        )

        session.add(depto)
        session.commit()

        print("-> Datos insertados con éxito.\n")

        stmt = select(Curso).where(Curso.titulo == "Álgebra Lineal")
        curso = session.scalars(stmt).first()

        if curso:
            print(f"Curso: {curso.titulo} | Profesor: {curso.profesor.nombre})")
            print("Clases registradas:")
            for clase in curso.clases:
                print(f" Tema: {clase.tema} | Duración: {clase.duracion_minutos} min")
  