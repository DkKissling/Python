import pygame
import random
import math
from pygame import mixer

# Inicializar Pygame
pygame.init()

# Crear pantalla
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Invasion Espacial")
icono = pygame.image.load("ovni.png")
pygame.display.set_icon(icono)

# Fondo
fondo = pygame.image.load("fondo.jpg")

mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# Jugador
img_jugador = pygame.image.load("cohete.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

# Enemigos
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("enemigo.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.2)
    enemigo_y_cambio.append(25)

# NUEVO: Lista para múltiples balas activas
balas = []

# Imagen de la bala (la misma para todas)
img_bala = pygame.image.load("bala.png")

# Puntaje
puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10

# Texto final del juego
fuente_final = pygame.font.Font('freesansbold.ttf', 40)

def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (200, 200))

# NUEVO: Texto de victoria
def texto_ganado():
    mi_fuente_ganado = fuente_final.render("¡JUEGO GANADO!", True, (0, 255, 0))
    pantalla.blit(mi_fuente_ganado, (220, 400))

def Jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

def Enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))

def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2))
    return distancia < 27

def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))

se_ejecuta = True

while se_ejecuta:
    pantalla.blit(fondo, (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -0.5
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.5

            # NUEVO: Disparo de bala múltiple al presionar ESPACIO
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound("disparo.mp3")
                sonido_bala.play()
                nueva_bala = {
                    "x": jugador_x,
                    "y": jugador_y,
                    "velocidad": -5
                }
                balas.append(nueva_bala)

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # Límite de pantalla del jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    # Enemigos
    for e in range(cantidad_enemigos):
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            balas.clear()  # NUEVO: Eliminar balas si se pierde
            break

        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.2
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.2
            enemigo_y[e] += enemigo_y_cambio[e]

        enemigo_x[e] += enemigo_x_cambio[e]

        # NUEVO: Detección de colisiones para cada bala activa
        for bala in balas:
            colision_bala_enemigo = hay_colision(enemigo_x[e], enemigo_y[e], bala["x"], bala["y"])
            if colision_bala_enemigo:
                sonido_colision = mixer.Sound("Golpe.mp3")
                sonido_colision.play()
                balas.remove(bala)
                puntaje += 1
                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(50, 200)
                break

        Enemigo(enemigo_x[e], enemigo_y[e], e)

    # NUEVO: Movimiento y dibujo de cada bala en la pantalla
    for bala in list(balas):
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)

    jugador_x += jugador_x_cambio

    mostrar_puntaje(texto_x, texto_y)
    Jugador(jugador_x, jugador_y)

    # NUEVO: Verificar si el jugador ganó al llegar a 20 puntos
    if puntaje >= 20:
        texto_ganado()
        for e in range(cantidad_enemigos):
            enemigo_y[e] = 1000
        balas.clear()

    pygame.display.update()
