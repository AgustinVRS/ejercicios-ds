from biblioteca.modelos.libro import libro
from datetime import date

class prestamo:
    def __init__(self,usuario,libro):
        self.libro = libro
        self.usuario = usuario
        self.fecha_prestamo = date.today()

    def realizarPrestamo(self, libro):
        disponible = libro.disponible
        if disponible == True:
            libro.disponible = False
            print("¡Se ha Realizado el Prestamo Con Exito!")    
        else:
            print("¡El libro no esta Disponible para Prestarlo!")

    def realizarDevolucion(self, libro):
        disponible = libro.disponible
        if disponible == False:
            libro.disponible = True
            print("¡Se ah realizado la devolucion con Exito!")
        else:
            print("!Libro Ya Disponible¡")

    def consultarDisponibilidad(self, libro):
        print(f"\nTitulo: {libro.titulo}| Autor: {libro.autor},")
        if libro.disponible == False:
            print("El libro No se Encuentra disponible :(\n")
        else:
            print("El libro Esta Disponible :)\n")
    