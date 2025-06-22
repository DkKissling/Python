import pygame
import random
import time
import json

# Inicializar Pygame
pygame.init()

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)

# Pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Tipea las Palabras")

# Fuente
fuente_texto = pygame.font.SysFont('Arial', 24)
fuente_instrucciones = pygame.font.SysFont('Arial', 20)

# Mostrar texto en pantalla
def mostrar_texto(texto, fuente, color, x, y):
    texto_renderizado = fuente.render(texto, True, color)
    pantalla.blit(texto_renderizado, (x, y))

# Mostrar texto largo ajustado al ancho
def mostrar_frase_formateada(frase, fuente, color, x, y, ancho_max):
    palabras = frase.split()
    linea = ""
    y_actual = y

    for palabra in palabras:
        prueba_linea = linea + palabra + " "
        ancho_texto, _ = fuente.size(prueba_linea)

        if ancho_texto <= ancho_max:
            linea = prueba_linea
        else:
            mostrar_texto(linea.strip(), fuente, color, x, y_actual)
            linea = palabra + " "
            y_actual += fuente.get_height() + 5

    if linea:
        mostrar_texto(linea.strip(), fuente, color, x, y_actual)

# Leer frases desde JSON
def cargar_frases_json(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["mensajes_confidenciales"]

# Seleccionar 5 palabras únicas al azar de una frase
def seleccionar_palabras(frase, cantidad=5):
    palabras = list(set(frase.replace(".", "").replace(",", "").replace(":", "").replace("-", "").split()))
    seleccionadas = random.sample(palabras, min(cantidad, len(palabras)))
    return seleccionadas

# Función principal del juego
def juego():
    ruta_json = r"C:\Users\usuario\Desktop\pygame-2\docs\confidencial.json"
    frases = cargar_frases_json(ruta_json)
    frase_elegida = random.choice(frases)
    palabras_a_tipear = seleccionar_palabras(frase_elegida, 5)

    palabra_actual_index = 0
    palabra_actual = palabras_a_tipear[palabra_actual_index]
    texto_ingresado = ""

    intentos_maximos = 5
    intentos_restantes = intentos_maximos
    tiempo_limite = 60
    tiempo_inicio = time.time()

    jugando = True

    while jugando:
        pantalla.fill(BLANCO)
        tiempo_transcurrido = time.time() - tiempo_inicio
        tiempo_restante = max(0, tiempo_limite - tiempo_transcurrido)

        if tiempo_restante == 0:
            jugando = False
            resultado = "¡Se acabó el tiempo! Perdiste."
        elif intentos_restantes == 0:
            jugando = False
            resultado = "¡Te quedaste sin intentos! Perdiste."
        elif palabra_actual_index >= len(palabras_a_tipear):
            jugando = False
            resultado = "¡Ganaste! Escribiste todas las palabras correctamente."

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    texto_ingresado = texto_ingresado[:-1]
                elif evento.key == pygame.K_RETURN:
                    if texto_ingresado.strip() == palabra_actual:
                        palabra_actual_index += 1
                        if palabra_actual_index < len(palabras_a_tipear):
                            palabra_actual = palabras_a_tipear[palabra_actual_index]
                        texto_ingresado = ""
                    else:
                        intentos_restantes -= 1
                        texto_ingresado = ""
                else:
                    texto_ingresado += evento.unicode
        mostrar_texto("Fragmentos de mensaje interceptado.Tipea todo antes de que se",fuente_texto,NEGRO,50,20)
        mostrar_texto("pierdan en el flujo de datos.",fuente_texto,NEGRO,50,50)

        if palabra_actual_index < len(palabras_a_tipear):
            mostrar_texto(f"Palabra: {palabra_actual}", fuente_texto, NEGRO, 50, 100)
        mostrar_texto("Tipea: " + texto_ingresado, fuente_texto, AZUL, 50, 150)
        mostrar_texto(f"Intentos restantes: {intentos_restantes}", fuente_texto, ROJO, 50, 250)
        mostrar_texto(f"Tiempo restante: {int(tiempo_restante)}s", fuente_texto, ROJO, 50, 300)
        mostrar_texto(f"Palabras restantes: {len(palabras_a_tipear) - palabra_actual_index}", fuente_texto, NEGRO, 50, 400)
        mostrar_texto("Presiona 'Enter' para verificar. 'Backspace' para borrar.", fuente_instrucciones, NEGRO, 50, 500)

        pygame.display.flip()
        pygame.time.Clock().tick(30)

    # Resultado final
    pantalla.fill(BLANCO)
    mostrar_texto(resultado, fuente_texto, NEGRO, 50, 100)

    if "Ganaste" in resultado:
        mostrar_texto("Frase completa original:", fuente_instrucciones, NEGRO, 50, 220)
        mostrar_frase_formateada(frase_elegida, fuente_instrucciones, NEGRO, 50, 260, 700)
    else:
        mostrar_texto("No lograste desbloquear el mensaje confidencial.", fuente_instrucciones, ROJO, 50, 220)


    pygame.display.flip()
    pygame.time.wait(7000)
    pygame.quit()

# Ejecutar el juego
juego()
