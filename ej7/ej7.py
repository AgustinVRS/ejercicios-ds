def analizar_temperaturas(temperaturas: list) -> tuple:
    return max(temperaturas), min(temperaturas), sum(temperaturas)/len(temperaturas)

if __name__ == "__main__":
    temperaturas = [10, 20, 40, 50, 60, 70, 80, 100, 0]
    maxima, minima, promedio = analizar_temperaturas(temperaturas)
    print(f"Maxima: {maxima} C°, Minima: {minima} C°, Promedio: {promedio} C°")

