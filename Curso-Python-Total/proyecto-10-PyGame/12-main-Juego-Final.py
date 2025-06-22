import pygame
import random
import math
from pygame import mixer

# inicializacion de pygame
pygame.init()

# configuracion de la pantalla
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Invasion Espacial")
icono = pygame.image.load("ovni.png")
pygame.display.set_icon(icono)

# cargar imagen de fondo
fondo = pygame.image.load("fondo.jpg")

# configuracion de musica de fondo
mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# variables del jugador
img_jugador = pygame.image.load("cohete.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

# variables de los enemigos
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

# inicializacion de enemigos
for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("enemigo.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.2)
    enemigo_y_cambio.append(25)

# variables de las balas
balas = []
img_bala = pygame.image.load("bala.png")

# variables del juego
puntaje = 0
objetivo_puntaje = 20  # puntaje necesario para ganar
juego_activo = True  # controla si el juego esta en curso
resultado_juego = None  # almacena "ganado" o "perdido"
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10

# fuentes para mensajes finales
fuente_final = pygame.font.Font('freesansbold.ttf', 40)
fuente_boton = pygame.font.Font('freesansbold.ttf', 24)

# funcion para reiniciar el juego
def reiniciar_juego():
    global jugador_x, jugador_y, jugador_x_cambio, puntaje, juego_activo, balas, resultado_juego

    # reiniciar posicion del jugador
    jugador_x = 368
    jugador_y = 500
    jugador_x_cambio = 0

    # reiniciar enemigos
    for e in range(cantidad_enemigos):
        enemigo_x[e] = random.randint(0, 736)
        enemigo_y[e] = random.randint(50, 200)

    # reiniciar variables del juego
    puntaje = 0
    juego_activo = True
    resultado_juego = None
    balas = []

# funcion para mostrar mensaje de juego terminado
def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (200, 200))

# funcion para mostrar mensaje de victoria
def texto_ganado():
    mi_fuente_ganado = fuente_final.render("¡JUEGO GANADO!", True, (0, 255, 0))
    pantalla.blit(mi_fuente_ganado, (220, 200))

# funcion para dibujar el boton de reinicio
def dibujar_boton():
    pygame.draw.rect(pantalla, (0, 200, 0), (300, 300, 200, 50))
    texto_boton = fuente_boton.render("REINICIAR", True, (255, 255, 255))
    pantalla.blit(texto_boton, (340, 310))
    return pygame.Rect(300, 300, 200, 50)  # retorna el rectangulo del boton para detectar clicks

# funcion para dibujar al jugador
def Jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

# funcion para dibujar enemigos
def Enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))

# funcion para detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2))
    return distancia < 27

# funcion para mostrar el puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}/{objetivo_puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))

# bucle principal del juego
se_ejecuta = True
boton_reinicio = None  # almacenara el rectangulo del boton de reinicio

while se_ejecuta:
    pantalla.blit(fondo, (0, 0))

    # manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        if juego_activo:
            # controles del jugador cuando el juego esta activo
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    jugador_x_cambio = -0.5
                if evento.key == pygame.K_RIGHT:
                    jugador_x_cambio = 0.5
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
        else:
            # manejo del boton de reinicio cuando el juego no esta activo
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_reinicio and boton_reinicio.collidepoint(evento.pos):
                    reiniciar_juego()

    if juego_activo:
        # limites del jugador
        jugador_x += jugador_x_cambio
        if jugador_x <= 0:
            jugador_x = 0
        elif jugador_x >= 736:
            jugador_x = 736

        # movimiento y comportamiento de los enemigos
        for e in range(cantidad_enemigos):
            # verificar si un enemigo llego al fondo (juego perdido)
            if enemigo_y[e] > 450:
                juego_activo = False
                resultado_juego = "perdido"
                break

            # cambio de direccion de los enemigos al llegar a los bordes
            if enemigo_x[e] <= 0:
                enemigo_x_cambio[e] = 0.2
                enemigo_y[e] += enemigo_y_cambio[e]
            elif enemigo_x[e] >= 736:
                enemigo_x_cambio[e] = -0.2
                enemigo_y[e] += enemigo_y_cambio[e]

            enemigo_x[e] += enemigo_x_cambio[e]

            # deteccion de colisiones entre balas y enemigos
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

        # verificar si se alcanzo el puntaje objetivo (juego ganado)
        if puntaje >= objetivo_puntaje:
            juego_activo = False
            resultado_juego = "ganado"

    # mostrar el resultado correspondiente
    if not juego_activo:
        if resultado_juego == "ganado":
            texto_ganado()
        else:
            texto_final()
        boton_reinicio = dibujar_boton()

    # movimiento de las balas
    for bala in list(balas):
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)

    # dibujar elementos del juego
    mostrar_puntaje(texto_x, texto_y)
    Jugador(jugador_x, jugador_y)

    pygame.display.update()
