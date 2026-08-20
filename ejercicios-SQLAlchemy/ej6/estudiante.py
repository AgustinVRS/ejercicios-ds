"""
Crear el modelo Estudiante (id, nombre, legajo). Como un
estudiante cursa muchas materias y una materia tiene muchos
alumnos, definir la tabla asociativa llamada Inscripcion para
conectar Estudiantes y Cursos.
Inscribir alumnos en diferentes cursos.
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

    inscripciones: Mapped[list["Inscripcion"]] = relationship(back_populates="curso") 

class Clase(Base):

    __tablename__ = "clases"

    id: Mapped[int] = mapped_column(primary_key=True)
    tema: Mapped[str] = mapped_column(String(50))
    duracion_minutos: Mapped[int] = mapped_column(Integer)

    curso_id: Mapped[int] = mapped_column(ForeignKey("cursos.id"))
    cursos: Mapped["Curso"] = relationship(back_populates="clases")

class Estudiante(Base):

    __tablename__ = "estudiantes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    legajo: Mapped[int] = mapped_column(Integer)

    inscripciones: Mapped[list["Inscripcion"]] = relationship(back_populates="estudiante")

class Inscripcion(Base):

    __tablename__ = "inscripciones"

    id: Mapped[int] = mapped_column(primary_key=True)

    estudiante_id: Mapped[int] = mapped_column(ForeignKey("estudiantes.id"))
    curso_id: Mapped[int] = mapped_column(ForeignKey("cursos.id"))

    fecha_inscripcion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    estudiante: Mapped["Estudiante"] = relationship(back_populates="inscripciones")
    curso: Mapped["Curso"] = relationship(back_populates="inscripciones")

    
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":

    with Session(engine) as session:
       
        depto = Departamento(nombre="Ciencias de la Computación")
        profe = Profesor(nombre="Alan Turing", email="alan.turing@unp.edu.ar", departamento=depto)

        curso_algo = Curso(titulo="Algoritmos y Estructuras de Datos", creditos=6.0, profesor=profe)
        curso_bd = Curso(titulo="Bases de Datos", creditos=4.0, profesor=profe)

        est_agustin = Estudiante(nombre="Agustin Vargas", legajo=10234)
        est_lucia = Estudiante(nombre="Lucia Gomez", legajo=10235)

        insc_1 = Inscripcion(estudiante=est_agustin, curso=curso_algo)
        insc_2 = Inscripcion(estudiante=est_agustin, curso=curso_bd)
        insc_3 = Inscripcion(estudiante=est_lucia, curso=curso_algo)

        # Guardar todas las entidades
        session.add_all([depto, profe, curso_algo, curso_bd, est_agustin, est_lucia, insc_1,insc_2, insc_3,])
        session.commit()

        print("Registros inscripciones guardados con éxito.\n")

        stmt_est = select(Estudiante).where(Estudiante.legajo == 10234)
        est = session.scalars(stmt_est).first()

        if est:
            print(f"Estudiante: {est.nombre} (Legajo: {est.legajo})")
            print("Materias cursadas:")
            for insc in est.inscripciones:
                print(
                    f" - {insc.curso.titulo} ({insc.curso.creditos} créditos) | Inscripto el: {insc.fecha_inscripcion.strftime('%Y-%m-%d %H:%M')}"
                )

        stmt_curso = select(Curso).where(Curso.titulo == "Algoritmos y Estructuras de Datos")
        curso = session.scalars(stmt_curso).first()

        if curso:
            print(f"Curso: {curso.titulo} (Prof. {curso.profesor.nombre})")
            print("Estudiantes inscriptos:")
            for insc in curso.inscripciones:
                print(f" - {insc.estudiante.nombre} (Legajo: {insc.estudiante.legajo})")