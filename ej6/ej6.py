def Operacion():
    print("---- MENU ----")
    print("1. Sumatoria de N numeros Naturales")
    print("2. Divison Por 3 Dentro de Un rango Numerico")
    print("3. Salir")
    n = input("Ingrese Operacion: ")

def sumarNumeros():
    numero = int(input("ingresar numero Natural: "))
    suma = 0
    for i in range(1, numero + 1):
        suma += i
        print(f"La Suma Total es: {suma}")

def dividirNumeros():
    inicial = int(input("Ingrese Numero Inicial: "))
    final = int(input("Ingrese Numero Final: "))
    for i in range(inicial, final + 1, 3):
        print(i)
    
if __name__ == "__main__":    
    numeros = Operacion()
    match numeros:
        case "1":
            sumarNumeros()
        case "2":
            dividirNumeros()
        case "3":
            print("Saliendo...")
        case _: 
            print("Opcion Invalida")