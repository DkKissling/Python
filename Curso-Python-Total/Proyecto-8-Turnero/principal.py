from Numeros.numeros import Turnero

def Menu():
    while True:
        print("""
        Bienvenido a SuperMarket
        Elija el área que desea y le daremos el turno correspondiente:
        
        1. Perfumeria
        2. Farmacia
        3. Cosmética
        4. Salir
        """)
        try:
            eleccion = int(input("Ingrese su opción (1-4): "))
        except ValueError:
            print(" Por favor, ingrese un número valido.")
            continue
        if eleccion in [1, 2, 3]:
            Turnero(eleccion)
            while True:
                repetir = input("\n¿Desea sacar otro turno? (s/n): ").strip().lower()
                if repetir == 's':
                    break
                elif repetir == 'n':
                    print("Gracias por su visita")
                    return
                else:
                    print(" Ingrese 's' para sí o 'n' para no.")
        elif eleccion == 4:
            print("Gracias por su visita")
            break
        else:
            print(" Opcion no valida. Ingrese un numero del 1 al 4.")

Menu()
   