nombre = input("Ingresa tu nombre: ")
ventas = float(input("Ingresa el total de tus ventas: "))

comision = ventas * 13 / 100

print(f"\n{nombre}, tu comisión de este mes es: ${comision:.2f}")
