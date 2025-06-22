def generador_turnos(prefijo):
    num = 0
    while True:
        yield f"{prefijo}-{num}"
        num += 1
opciones = {
    1: generador_turnos("P"),
    2: generador_turnos("F"),
    3: generador_turnos("C")
}
def Saludo(funcion):
    def wrapper(*args):
        turno = funcion(*args)
        print(f"Su turno es: {turno}")
        print("Aguarde y será atendido.")
        return turno
    return wrapper
@Saludo
def Turnero(opcion):
    return next(opciones[opcion])

