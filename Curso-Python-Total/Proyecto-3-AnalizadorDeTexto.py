texto = input("Ingresa un texto: ").lower()

letra1 = input("Ingresa la primera letra: ").lower()
letra2 = input("Ingresa la segunda letra: ").lower()
letra3 = input("Ingresa la tercera letra: ").lower()

conteo1 = texto.count(letra1)
conteo2 = texto.count(letra2)
conteo3 = texto.count(letra3)

palabras = texto.split()
cantidad_palabras = len(palabras)

primera_letra = texto[0]
ultima_letra = texto[-1]

texto_invertido = " ".join(palabras[::-1])

contiene_python = "sí" if "python" in texto else "no"

print("\nAnálisis del texto:")
print(f"La letra '{letra1}' aparece {conteo1} veces.")
print(f"La letra '{letra2}' aparece {conteo2} veces.")
print(f"La letra '{letra3}' aparece {conteo3} veces.")
print(f"El texto tiene {cantidad_palabras} palabras.")
print(f"La primera letra es '{primera_letra}' y la última es '{ultima_letra}'.")
print(f"Texto invertido: {texto_invertido}")
print(f"¿El texto menciona 'Python'? {contiene_python}.")
