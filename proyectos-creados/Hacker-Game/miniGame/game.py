import pygame
import random
from BruteForce2 import mostrar_texto, jugar_ronda, cargar_palabras_y_pistas_json
import os

# Inicializamos pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fuerza Bruta: Adivina Contraseñas con Pistas")
font = pygame.font.SysFont(None, 36)

# Cargar las palabras y pistas desde el archivo JSON
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_json = os.path.join(directorio_actual, "../docs/palabras.json")

palabras_pistas = cargar_palabras_y_pistas_json(ruta_json)

# Seleccionar una palabra y su pista aleatoriamente
palabra = random.choice(list(palabras_pistas.keys()))
pista = palabras_pistas[palabra]

# Llamada al juego con los parámetros deseados
jugar_ronda(
    palabra=palabra,
    pista=pista,
    screen=screen,
    font=font,
    max_errores=6,
    pos_x=50,
    pos_y=40,
    color_fondo=(30, 30, 30)
)

# Mostrar mensaje de agradecimiento al final
mostrar_texto("¡Gracias por jugar!", 100, 100, screen, font, color=(255, 255, 0))
pygame.display.flip()
pygame.time.wait(3000)
pygame.quit()
