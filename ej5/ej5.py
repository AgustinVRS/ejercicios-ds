if __name__ == "__main__":
    valida = False
    while (not valida):

        contrasenia = input("Ingrese la contraseña: ")

        mayusculas = any(c.isupper() for c in contrasenia)
        minisculas = any (c.islower() for c in contrasenia)
        longitud = len(contrasenia) >= 8

        if mayusculas and minisculas and longitud:
            print("La contraseña es válida.")
            valida = True
        else:
            print("La contraseña no es válida. Debe contener al menos una letra mayúscula, una letra minúscula y tener una longitud mínima de 8 caracteres.")
