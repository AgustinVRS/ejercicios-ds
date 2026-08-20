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
from sqlalchemy import String, ForeignKey, DateTime, select,Float,Integer, CheckConstraint, func
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

    id: Mapped[int] = mapped_column(primary_key=True)
    fecha_inscripcion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    calificacion_final: Mapped[Optional[float]] = mapped_column(Float, CheckConstraint("calificacion_final >= 0 AND calificacion_final <= 10"), nullable=True) 

    estudiante_id: Mapped[int] = mapped_column(ForeignKey("estudiantes.id"))
    curso_id: Mapped[int] = mapped_column(ForeignKey("cursos.id"))

    estudiante: Mapped["Estudiante"] = relationship(back_populates="inscripciones")
    curso: Mapped["Curso"] = relationship(back_populates="inscripciones")

    
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":

    with Session(engine) as session:

        depto_exactas = Departamento(nombre="Ciencias Exactas")
        
        prof_turing = Profesor(nombre="Alan Turing", email="alan.turing@unp.edu.ar", departamento=depto_exactas)
        prof_lovelace = Profesor(nombre="Ada Lovelace", email="ada.lovelace@unp.edu.ar", departamento=depto_exactas)

        curso_bd = Curso(titulo="Bases de Datos", creditos=4.0, profesor=prof_turing)
        curso_algo = Curso(titulo="Algoritmos I", creditos=6.0, profesor=prof_turing)
        curso_so = Curso(titulo="Sistemas Operativos", creditos=5.0, profesor=prof_lovelace)

        est_1 = Estudiante(nombre="Agustin Vargas", legajo=10234)
        est_2 = Estudiante(nombre="Lucia Gomez", legajo=10235)
        est_3 = Estudiante(nombre="Carlos Ruiz", legajo=10236)

        insc_1 = Inscripcion(estudiante=est_1, curso=curso_bd, calificacion_final=9.0)
        insc_2 = Inscripcion(estudiante=est_1, curso=curso_algo, calificacion_final=7.5)
        insc_3 = Inscripcion(estudiante=est_2, curso=curso_bd, calificacion_final=8.0)
        insc_4 = Inscripcion(estudiante=est_3, curso=curso_algo, calificacion_final=6.0)

        session.add_all([depto_exactas, prof_turing, prof_lovelace, curso_bd, curso_algo, curso_so, est_1, est_2, est_3, insc_1, insc_2, insc_3, insc_4])
        session.commit()
        print("Registros iniciales insertados correctamente.\n")

        print("--- REPORTE 1: Cursos de Alan Turing (usando join) ---")
        stmt_rep1 = (select(Curso).join(Curso.profesor).where(Profesor.email == "alan.turing@unp.edu.ar"))
        cursos_profesor = session.scalars(stmt_rep1).all()
        for c in cursos_profesor:
            print(f" • {c.titulo} ({c.creditos} créditos)")

        print("\n" + "=" * 55 + "\n")

        print("--- REPORTE 2: Promedio de Agustin Vargas (func.avg) ---")
        stmt_rep2 = (select(func.avg(Inscripcion.calificacion_final)).join(Inscripcion.estudiante).where(Estudiante.legajo == 10234).where(Inscripcion.calificacion_final.is_not(None)))
        promedio = session.scalar(stmt_rep2)
        if promedio is not None:
            print(f"Promedio de calificaciones: {promedio:.2f}")
        else:
            print("No registra calificaciones.")

        print("\n" + "=" * 55 + "\n")

        print("--- REPORTE 3: Estudiantes inscriptos por curso (func.count) ---")
        stmt_rep3 = (select(Curso.titulo, func.count(Inscripcion.estudiante_id).label("total_inscriptos")).outerjoin(Curso.inscripciones).group_by(Curso.id, Curso.titulo))
        conteos = session.execute(stmt_rep3).all()
        for titulo, total in conteos:
            print(f" • {titulo}: {total} alumno(s)")