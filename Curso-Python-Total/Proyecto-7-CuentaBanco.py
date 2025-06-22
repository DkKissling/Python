class Persona:
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido

class Cliente(Persona):
    def __init__(self, nombre, apellido, nroCuenta):
        super().__init__(nombre, apellido)
        self.nroCuenta = nroCuenta
        self.balance = 0 
    def __str__(self):
        return (f"Nombre: {self.nombre}, Apellido: {self.apellido}, "
                f"NroCuenta: {self.nroCuenta}, Balance: {self.balance}")  # self.balance

    def Depositar(self, deposito):
        self.balance += deposito  
        return self.balance

    def Retirar(self, retiro):
        if retiro > self.balance: 
            print("El retiro es mayor al dinero disponible en la cuenta.")
        else:
            self.balance -= retiro
        return self.balance

def crear_cliente():
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    nroCuenta = input("Número de cuenta: ")
    return Cliente(nombre, apellido, nroCuenta)

def Inicio():
    cliente = crear_cliente()
    opcion = 0
    while opcion != 3:
        print("\nElige una opción:\n 1. Depositar\n 2. Retirar\n 3. Salir")         
        try:
            opcion = int(input("Opción: "))
            if opcion == 1:
                try:
                    deposito = int(input("¿Cuánto desea depositar? "))
                    cliente.Depositar(deposito)
                    print("Depósito exitoso.")
                    print(cliente)
                except ValueError:
                    print("Ingrese un número válido para el depósito.")
            elif opcion == 2:
                try:
                    retiro = int(input("¿Cuánto desea retirar? "))
                    cliente.Retirar(retiro)
                    print(cliente)
                except ValueError:
                    print("Ingrese un número válido para el retiro.")
            elif opcion == 3:
                print("Gracias por usar nuestro sistema")
            else:
                print("Ingrese una opción válida")
        except ValueError:
            print("Ingrese un número válido para la opción.")

Inicio()