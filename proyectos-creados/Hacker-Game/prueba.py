import pygame
import random
import time
import os

# Inicializar Pygame
pygame.init()
WIDTH, HEIGHT = 800, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mecanografía Hacker")

# Colores y fuentes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
font_large = pygame.font.SysFont("Courier New", 40, bold=True)
font_small = pygame.font.SysFont("Arial", 20)

# Cargar palabras desde un archivo
def cargar_palabras():
    try:
        ruta = os.path.join(os.path.dirname(__file__), 'docs', "palabras.txt")
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read()
            
            # Verificar si el contenido tiene comas (formato: "word1, word2, word3")
            if ',' in contenido:
                # Dividir por comas y eliminar espacios en blanco
                palabras = [palabra.strip() for palabra in contenido.split(',')]
            else:
                # Formato normal: una palabra por línea
                palabras = [line.strip() for line in contenido.splitlines() if line.strip()]
                
            # Eliminar elementos vacíos
            palabras = [p for p in palabras if p]
            print(f"Palabras cargadas: {palabras}")  # Depuración
            return palabras
    except FileNotFoundError:
        print("¡Error! No se encontró 'palabras.txt'")
        return ["python"]  # Palabra predeterminada si no hay archivo

# Cargar todas las palabras una vez
todas_palabras = cargar_palabras()
palabras_usadas = []  # Para seguimiento de palabras ya utilizadas

# Función para seleccionar una sola palabra a la vez
def seleccionar_palabra():
    global palabras_usadas, todas_palabras
    
    if not todas_palabras:
        return "python"  # Palabra predeterminada si no hay palabras
    
    # Elegir una palabra aleatoria de la lista
    palabra = random.choice(todas_palabras)
    return palabra

# Variables del juego
palabra_actual = seleccionar_palabra()
input_usuario = ""
vidas = 3
puntaje = 0
tiempo_inicial = time.time()
tiempo_limite = 5  # Segundos por palabra
game_over = False

def nueva_palabra():
    global palabra_actual, input_usuario, tiempo_inicial
    palabra_actual = seleccionar_palabra()
    input_usuario = ""
    tiempo_inicial = time.time()

# Bucle principal
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if input_usuario == palabra_actual:
                    puntaje += 1
                    nueva_palabra()
                else:
                    vidas -= 1
                    if vidas <= 0:
                        print("¡Descubierto!")
                        game_over = True
                    else:
                        nueva_palabra()
            elif event.key == pygame.K_BACKSPACE:
                input_usuario = input_usuario[:-1]
            else:
                input_usuario += event.unicode

    # Dibujar interfaz
    texto_palabra = font_large.render(palabra_actual, True, GREEN)
    screen.blit(texto_palabra, (WIDTH // 2 - texto_palabra.get_width() // 2, 100))

    texto_input = font_large.render(input_usuario, True, WHITE)
    screen.blit(texto_input, (WIDTH // 2 - texto_input.get_width() // 2, 150))

    tiempo_restante = max(0, tiempo_limite - (time.time() - tiempo_inicial))
    texto_tiempo = font_small.render(f"Tiempo: {tiempo_restante:.1f}s", True, WHITE)
    screen.blit(texto_tiempo, (20, 20))

    texto_vidas = font_small.render(f"Vidas: {vidas}", True, RED if vidas == 1 else WHITE)
    screen.blit(texto_vidas, (WIDTH - 150, 20))

    texto_puntaje = font_small.render(f"Puntaje: {puntaje}", True, WHITE)
    screen.blit(texto_puntaje, (WIDTH - 150, 50))

    # Verificar tiempo
    if not game_over and tiempo_restante <= 0:
        vidas -= 1
        if vidas <= 0:
            print("¡Descubierto!")
            game_over = True
        else:
            nueva_palabra()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()