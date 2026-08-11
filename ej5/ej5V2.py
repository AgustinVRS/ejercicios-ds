if __name__ == "__main__":
    PASSWORD = "Admin1234"
    valida = False

    while (not valida):

        contrasenia = input("Ingrese la contraseña: ")
        if contrasenia == PASSWORD:
            print("La contraseña es correcta.")
            valida = True
        else:
            print("La contraseña es incorrecta. Intente nuevamente.")