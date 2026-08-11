def calcular_precio_final(precio_base, porcentaje_descuento = 10, es_vip=False) -> float:
    if precio_base <= 0 or porcentaje_descuento < 0: 
        raise ValueError("El Precio Base y el Descuento deben ser mayores a 0")
    
    precio = precio_base * (1 - porcentaje_descuento/100)

    if es_vip:
        precio *= (1 - 5/100)

    return precio    

if __name__ == "__main__":
    try:
        total = calcular_precio_final(1000,10,True)
        print(f"precio total: {total}")
    except ValueError as e:
        print(f"Error en Prueba 1: {e}")

    try:   
        total2 = calcular_precio_final(0,10,False)
        print(f"Precio Total: {total}")
    except ValueError as e:
        print(f"Error en Prueba 2: {e}")
