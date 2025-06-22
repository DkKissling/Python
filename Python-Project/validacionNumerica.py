
Escribe una función en Python que solicite al usuario ingresar un número real (entero o decimal) con las siguientes características:

La función debe mostrar un mensaje personalizado al solicitar el número.
Debe permitir especificar un rango válido para el número (mínimo y máximo).
Debe validar que la entrada del usuario sea un número real válido. Si la entrada no es un número válido, la función debe mostrar un mensaje de error y solicitar el ingreso nuevamente.
Debe permitir una validación personalizada mediante una función de callback proporcionada por el usuario.
Debe permitir un número máximo de intentos para ingresar un valor válido. Si se excede este número de intentos, la función debe terminar y retornar None.
Debe permitir al usuario continuar intentando después de exceder el número máximo de intentos, si así se configura.
Debe permitir al usuario ingresar una cadena especial (como "salir" o "cancelar") para terminar la función sin ingresar un número.
Debe permitir al usuario ingresar valores negativos o limitar la entrada a solo valores positivos.
Debe permitir al usuario ingresar un número con notación científica (por ejemplo, "1e-3" para 0.001).
Debe manejar adecuadamente los casos de entrada vacía (solo espacios en blanco) y mostrar mensajes de error claros al usuario.
Debe tener una opción para habilitar un historial de todas las entradas del usuario en lugar de retornar solo el número final.
Debe validar que los parámetros proporcionados a la función (como el rango y el número máximo de intentos) sean válidos y manejar adecuadamente los casos en los que no lo sean.
Debe proporcionar una documentación clara y ejemplos de uso para ilustrar el comportamiento esperado de la función.

Escribe una función que cumpla con estos requisitos y proporciona ejemplos de uso que demuestren las diferentes configuraciones y casos de uso.

import re
from typing import Callable, Union, Tuple

def validar_rango(rango: Union[Tuple[float, float], None]) -> Tuple[float, float] or None:
    """
    Valida que el rango sea una tupla de dos elementos y los convierte a flotantes.
    Si el rango es None, devuelve None.
    """
    if rango is None:
        return None
    try:
        minimo, maximo = [float(x) for x in rango]
        if minimo > maximo:
            raise ValueError("El valor mínimo no puede ser mayor que el máximo.")
        return minimo, maximo
    except (ValueError, TypeError):
        raise ValueError("El rango debe ser una tupla de dos números reales.")

def validar_intentos_max(intentos_max: int) -> int:
    """
    Valida que intentos_max sea un número entero positivo.
    """
    try:
        intentos_max = int(intentos_max)
        if intentos_max <= 0:
            raise ValueError("El número máximo de intentos debe ser un entero positivo.")
        return intentos_max
    except ValueError:
        raise ValueError("El número máximo de intentos debe ser un entero positivo.")

def obtener_numero_real(mensaje: str = "Ingrese un número real: ",
                        rango: Union[Tuple[float, float], None] = None,
                        intentos_max: int = 3,
                        validacion_personalizada: Callable[[float], bool] = None,
                        mensaje_excedido: str = None,
                        continuar_despues_excedido: bool = False,
                        historial_entradas: bool = False,
                        permitir_negativo: bool = True,
                        permitir_especial: str = None) -> Union[float, list[str], None]:

    rango = validar_rango(rango)
    intentos_max = validar_intentos_max(intentos_max)

    historial = []
    for intento in range(1, intentos_max + 1):
        entrada = input(mensaje).strip()
        historial.append(entrada)

        if permitir_especial and entrada == permitir_especial:
            if historial_entradas:
                return historial
            return None

        if entrada == "":
            print("No ha ingresado ningún valor. Inténtelo de nuevo.")
            continue

        try:
            numero = float(entrada)
            if not permitir_negativo and numero < 0:
                raise ValueError("No se permiten números negativos.")
            if rango is not None:
                minimo, maximo = rango
                if numero < minimo or numero > maximo:
                    raise ValueError(f"El número debe estar entre {minimo} y {maximo}.")
            if validacion_personalizada is not None and not validacion_personalizada(numero):
                raise ValueError("La entrada no cumple con la validación personalizada.")
            return numero
        except ValueError as e:
            print(f"Error: {e}. Inténtelo de nuevo.")
        except TypeError:
            print(f"Error: '{entrada}' no es un número válido. Inténtelo de nuevo.")

    if mensaje_excedido:
        print(mensaje_excedido)

    if continuar_despues_excedido:
        respuesta = input("¿Desea continuar? (s/n): ")
        if respuesta.lower() == 's':
            return obtener_numero_real(mensaje, rango, intentos_max, validacion_personalizada,
                                       mensaje_excedido, continuar_despues_excedido,
                                       historial_entradas, permitir_negativo, permitir_especial)

    if historial_entradas:
        return historial

    return None

# Ejemplo de uso
def validacion_personalizada(numero):
    return numero % 2 == 0  # El número debe ser par

numero1 = obtener_numero_real("Ingrese un número entre 0 y 10: ", rango=(0, 10), intentos_max=5)
if numero1 is not None:
    print(f"El número ingresado es: {numero1}")
else:
    print("No se ingresó un número válido.")

numero2 = obtener_numero_real(mensaje_excedido="No se ingresó un número válido.",
                               intentos_max=2, validacion_personalizada=validacion_personalizada,
                               permitir_negativo=False, permitir_especial="salir")
if numero2 is not None:
    print(f"El número ingresado es: {numero2}")
else:
    print("No se ingresó un número válido.")

historial = obtener_numero_real(historial_entradas=True)
print(f"Historial de entradas: {historial}")
