"""
Transformar la tabla asociativa anterior para añadir los atributos
fecha_inscripcion y calificacion_final.
Modificar las relaciones en Estudiante y Curso utilizando
secondary o mapeo directo para mantener la relación
Many-to-Many enriquecida.
"""

from typing import Optional
from datetime import datetime
from database import Base, engine
from sqlalchemy import String, ForeignKey, DateTime, select,Float,Integer, CheckConstraint, func, UniqueConstraint
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship
from sqlalchemy.exc import IntegrityError

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
    estudiantes: Mapped[list["Estudiante"]] = relationship(secondary="inscripciones", back_populates="cursos", viewonly=True) 

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

    cursos: Mapped[list["Curso"]] = relationship(secondary="inscripciones", back_populates="estudiantes", viewonly=True)

class Inscripcion(Base):

    __tablename__ = "inscripciones"
    __table_args__ = (UniqueConstraint("estudiante_id", "curso_id", name="uq_estudiante_curso"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    fecha_inscripcion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    calificacion_final: Mapped[Optional[float]] = mapped_column(Float, CheckConstraint("calificacion_final >= 0 AND calificacion_final <= 10"), nullable=True) 

    estudiante_id: Mapped[int] = mapped_column(ForeignKey("estudiantes.id"))
    curso_id: Mapped[int] = mapped_column(ForeignKey("cursos.id"))

    estudiante: Mapped["Estudiante"] = relationship(back_populates="inscripciones")
    curso: Mapped["Curso"] = relationship(back_populates="inscripciones")
    
Base.metadata.create_all(bind=engine)

def matricular_alumno(session: Session, legajo: int, curso_id: int, calificacion: Optional[float] = None,) -> bool:
    try:
        stmt_est = select(Estudiante).where(Estudiante.legajo == legajo)
        estudiante = session.scalars(stmt_est).first()
        if not estudiante:
            raise ValueError(f"No existe estudiante con legajo {legajo}")

        stmt_curso = select(Curso).where(Curso.id == curso_id)
        curso = session.scalars(stmt_curso).first()
        if not curso:
            raise ValueError(f"No existe curso con ID {curso_id}")

        nueva_inscripcion = Inscripcion(estudiante=estudiante,curso=curso,calificacion_final=calificacion)
        session.add(nueva_inscripcion)
        session.commit()
        print(f"Matrícula exitosa: {estudiante.nombre} inscripto en '{curso.titulo}'.")
        return True

    except IntegrityError as err:
        session.rollback()
        print(f"Error de integridad en la BD (Rollback ejecutado): {err.orig}")
        return False

    except Exception as err:
        session.rollback()
        print(f"Error lógico en la operación (Rollback ejecutado): {err}")
        return False
    
if __name__ == "__main__":

    with Session(engine) as session:

        depto = Departamento(nombre="Informática")
        prof = Profesor(nombre="Alan Turing",email="alan.turing@unp.edu.ar",departamento=depto)
        curso_bd = Curso(titulo="Bases de Datos", creditos=4.0, profesor=prof)
        estudiante_1 = Estudiante(nombre="Agustin Vargas", legajo=10234)

        session.add_all([depto, prof, curso_bd, estudiante_1])
        session.commit()

        print("--- PRUEBA 1: Matrícula inicial válida ---")
        matricular_alumno(session, legajo=10234, curso_id=curso_bd.id)

        print("\n--- PRUEBA 2: Forzar excepción por inscripción duplicada ---")
        matricular_alumno(session, legajo=10234, curso_id=curso_bd.id)

        print("\n--- PRUEBA 3: Forzar excepción por CheckConstraint (nota 15) ---")
        curso_algo = Curso(titulo="Algoritmos I", creditos=6.0, profesor_id=prof.id)
        session.add(curso_algo)
        session.commit()

        matricular_alumno(session, legajo=10234, curso_id=curso_algo.id, calificacion=15.0)

        print("\n--- VERIFICACIÓN MANUAL EN LA BD ---")
        stmt_verificacion = select(Inscripcion).where(Inscripcion.estudiante_id == estudiante_1.id)
        inscripciones_actuales = session.scalars(stmt_verificacion).all()

        print(f"Total de inscripciones persistidas en la BD: {len(inscripciones_actuales)}")
        for ins in inscripciones_actuales:
            print(f" - Curso ID: {ins.curso_id} | Calificación: {ins.calificacion_final}")