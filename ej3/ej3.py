if __name__ == "__main__":

    costo_pasaje = float(input("Ingrese el costo del pasaje: "))
    costo_alojamiento = float(input("Ingrese el costo del alojamiento: "))
    cant_noches = int(input("Ingrese la cantidad de noches: "))
    dinero_disponible = float(input("Ingrese el dinero disponible: "))

    costo_total = costo_pasaje + (costo_alojamiento * cant_noches)
    alcanza_dinero = dinero_disponible >= costo_total

    print("\n--- DATOS DEL VIAJE ---")
    print(f"Costo del pasaje: ${costo_pasaje:.2f}")
    print(f"Costo del alojamiento por noche: ${costo_alojamiento:.2f}")
    print(f"Cantidad de noches: {cant_noches}")
    print(f"Dinero disponible: ${dinero_disponible:.2f}")
    print(f"Costo total del viaje: ${costo_total:.2f}")
    print(f"¿Alcanza el dinero disponible para cubrir los costos del viaje? {'Sí' if alcanza_dinero else 'No'}")

    if not alcanza_dinero:
        print("No hay suficiente dinero disponible para cubrir los costos del viaje.")
    else:
        print("Hay suficiente dinero disponible para cubrir los costos del viaje.")