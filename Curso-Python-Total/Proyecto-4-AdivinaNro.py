import random

nombre = input("¿Cuál es tu nombre?: ")

numero_aleatorio = random.randint(1, 100)

print(f"Hola, {nombre}, he pensado un número entre 1 y 100, y tienes solo ocho intentos para adivinar cuál es.")

for i in range(8):
    numero = input("Dime qué número estoy pensando: ")
    
    try:
        numero = int(numero)
    except ValueError:
        print("¡Eso no es un número! Por favor, ingresa un número válido.")
        continue  
    
    if numero < 1 or numero > 10:
        print("El número debe estar entre 1 y 100. Intenta nuevamente.")
        continue
    
    if numero < numero_aleatorio:
        print("Tu número es menor que el número secreto. ¡Intenta nuevamente!")
    elif numero > numero_aleatorio:
        print("Tu número es mayor que el número secreto. ¡Intenta nuevamente!")
    else:
        print(f"¡Felicidades, {nombre}! Adivinaste el número secreto, que era {numero_aleatorio}. ¡Lo lograste en {i + 1} intentos!")
        break  

if numero != numero_aleatorio:
    print(f"Lo siento, {nombre}, no adivinaste el número. El número secreto era {numero_aleatorio}.")
