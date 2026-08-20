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
from sqlalchemy import String, ForeignKey, DateTime, select,Float,Integer, CheckConstraint
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
        
        depto = Departamento(nombre="Informática")
        prof = Profesor(nombre="Alan Turing", email="alan.turing@unp.edu.ar", departamento=depto)

        curso_bd = Curso(titulo="Bases de Datos", creditos=4.0, profesor=prof)
        curso_algo = Curso(titulo="Algoritmos I", creditos=6.0, profesor=prof)

        est_1 = Estudiante(nombre="Agustin Vargas", legajo=10234)
        est_2 = Estudiante(nombre="Lucia Gomez", legajo=10235)

        i1 = Inscripcion(estudiante=est_1, curso=curso_bd, calificacion_final=9.5)
        i2 = Inscripcion(estudiante=est_1, curso=curso_algo, calificacion_final=8.0)
        i3 = Inscripcion(estudiante=est_2, curso=curso_bd, calificacion_final=None)

        session.add_all([depto, prof, curso_bd, curso_algo, est_1, est_2, i1, i2, i3])
        session.commit()
        print("Registros guardados correctamente.\n")

        stmt_est = select(Estudiante).where(Estudiante.legajo == 10234)
        est = session.scalars(stmt_est).first()

        if est:
            print(f"Acceso Directo: {est.nombre}")
            for c in est.cursos:
                print(f"Curso: {c.titulo} ({c.creditos} créditos)")

        if est:
            print(f"Acceso Enriquecido: {est.nombre}")
            for insc in est.inscripciones:
                nota = insc.calificacion_final if insc.calificacion_final is not None else "En cursada"
                print(f"{insc.curso.titulo} | Nota: {nota} | Inscripto el: {insc.fecha_inscripcion.strftime('%Y-%m-%d')}")