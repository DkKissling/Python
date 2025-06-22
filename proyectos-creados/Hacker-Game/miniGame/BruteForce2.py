# juego.py
import pygame
import json
import random
import sys


# Función para cargar las palabras y pistas desde un archivo JSON
def cargar_palabras_y_pistas_json(archivo):
    with open(archivo, "r") as file:
        return json.load(file)

# Función para mostrar texto en pantalla
def mostrar_texto(texto, x, y, screen, font, color=(255, 255, 255)):
    img = font.render(texto, True, color)
    screen.blit(img, (x, y))

# Función que maneja la lógica del juego
def jugar_ronda(palabra, pista, screen, font, max_errores=5, pos_x=20, pos_y=20, color_fondo=(0,0,0)):
    clock = pygame.time.Clock()

    intento = ""  # Cadena donde se almacena lo que el jugador está escribiendo
    errores = 0
    juego_terminado = False
    mensaje_final = ""
    letras_correctas = ["_" for _ in palabra]

    # Bucle principal del juego
    while True:
        screen.fill(color_fondo)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not juego_terminado:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if intento == palabra:
                            letras_correctas = list(palabra)
                            mensaje_final = "🎉 ¡Ganaste!"
                            juego_terminado = True
                        else:
                            for i in range(min(len(intento), len(palabra))):
                                if intento[i] == palabra[i]:
                                    letras_correctas[i] = intento[i]
                            errores += 1
                            intento = ""
                            if errores >= max_errores:
                                mensaje_final = f"💀 ¡Perdiste! Era '{palabra}'"
                                juego_terminado = True
                    elif event.key == pygame.K_BACKSPACE:
                        intento = intento[:-1]
                    else:
                        letra = event.unicode.lower()
                        if letra.isalpha():
                            intento += letra

        mostrar_texto("🔤 Adivina la Contraseña", pos_x, pos_y, screen, font)
        mostrar_texto(f"Pista: {pista}", pos_x, pos_y + 60, screen, font)
        mostrar_texto(f"Letras: {' '.join(letras_correctas)}", pos_x, pos_y + 120, screen, font)
        mostrar_texto(f"Intento: {intento}", pos_x, pos_y + 180, screen, font)
        mostrar_texto(f"Errores: {errores} / {max_errores}", pos_x, pos_y + 240, screen, font)

        if juego_terminado:
            color = (0, 255, 0) if "Ganaste" in mensaje_final else (255, 0, 0)
            mostrar_texto(mensaje_final, pos_x, pos_y + 300, screen, font, color)

        pygame.display.flip()
        clock.tick(30)
