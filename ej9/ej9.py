class CuentaBancaria:
    def __init__(self,titular,saldo):
        self.titular = titular
        self.saldo = saldo

    def depositar(self,monto):
        if monto > 0:
            self.saldo += monto
            print("¡Se deposito Exitosamente!")
        else:
            raise ValueError("Su deposito debe ser mayor a 0")

    def retirar(self,monto):
        if monto <= 0 or monto > self.saldo:
            raise ValueError("No hay fondo suficiente para retirar")
        else:
            self.saldo -= monto
            print("¡Se ha extraido dinero Exitosamente!")

    def mostrar_info(self):
        print(f"TITULAR: {self.titular} | SALDO: {self.saldo}")

if __name__ == "__main__":

    cuenta1 = CuentaBancaria("Agustin", 3000)
    cuenta2 = CuentaBancaria("Facu",0)
    
    try:
         cuenta1.retirar(300)       
    except ValueError as e:
        print(e)
    try:
        cuenta1.depositar(100)
    except ValueError as e:
        print(e)
    cuenta1.mostrar_info()


    try:
        cuenta2.depositar(0)
    except ValueError as e:
        print(e)
    try:
        cuenta2.retirar(100)
    except ValueError as e:
        print(e)
    cuenta2.mostrar_info()


    