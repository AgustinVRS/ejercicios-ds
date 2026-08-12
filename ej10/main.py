from biblioteca.modelos.libro import libro
from biblioteca.servicios.prestamo import prestamo


libro1 = libro("Harry Potter","Julio Borges","ESTA PIOLA")
libro1.disponible = False

libro2 = libro("Somos Nosotros","Julio Borges","ESTA RE FEO")
libro2.disponible = True

mi_prestamo = prestamo("Agustin", libro1)

mi_prestamo.realizarPrestamo(libro1)
mi_prestamo.realizarDevolucion(libro1)
mi_prestamo.consultarDisponibilidad(libro1)

mi_prestamo2 = prestamo("Lucas", libro2)

mi_prestamo2.realizarPrestamo(libro2)
mi_prestamo2.consultarDisponibilidad(libro2)