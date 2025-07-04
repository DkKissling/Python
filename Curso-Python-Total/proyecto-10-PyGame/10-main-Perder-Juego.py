import pygame
import random
import math
from pygame import mixer

pygame.init()

pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Invasion Espacial")
icono = pygame.image.load("ovni.png")
pygame.display.set_icon(icono)

fondo = pygame.image.load("fondo.jpg")

#mixer.music.load('MusicaFondo.mp3')
#mixer.music.set_volume(0.3)
#mixer.music.play(-1)

img_jugador = pygame.image.load("cohete.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

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

img_bala = pygame.image.load("bala.png")
bala_x = 0
bala_y = 500
bala_y_cambio = 2
bala_visible = False

puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10

#Texto final del Juego 
fuente_final=pygame.font.Font('freesansbold.ttf',40)
def texto_final():
    mi_fuente_final=fuente_final.render("JUEGO TERMINADO",True, (255,255,255))
    pantalla.blit(mi_fuente_final,(100,200))

def Jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

def Enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))

def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))

def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        return False

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
            if evento.key == pygame.K_SPACE and not bala_visible:
                sonido_bala = mixer.Sound('disparo.mp3')
                sonido_bala.play()
                bala_x = jugador_x
                disparar_bala(bala_x, bala_y)

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    for e in range(cantidad_enemigos):
#FIN DEL JUEGO PORQUE PERDIO- revisamos si algun enemigo esta en la posicion Y = 250 que donde esta nuestra nave
        if enemigo_y[e]>400:
#Si alguno llego Sacamos a todos los enemigos que estan en la pantalla de la vista- para eso los mandamos a la posicion 1000 para que ya no se vean
            for k in range(cantidad_enemigos):
                enemigo_y[k]=1000
#llamamos la funcion texto_final para que se muestre
            texto_final()
            break



        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.2
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.2
            enemigo_y[e] += enemigo_y_cambio[e]

        enemigo_x[e] += enemigo_x_cambio[e]

        colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision:
            sonido_colision = mixer.Sound('Golpe.mp3')
            sonido_colision.play()
            bala_y = 500
            bala_visible = False
            puntaje += 1
            enemigo_x[e] = random.randint(0, 736)
            enemigo_y[e] = random.randint(50, 200)

        Enemigo(enemigo_x[e], enemigo_y[e], e)

    if bala_y <= -64:
        bala_y = 500
        bala_visible = False

    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio

    jugador_x += jugador_x_cambio

    mostrar_puntaje(texto_x, texto_y)

    Jugador(jugador_x, jugador_y)
    pygame.display.update()
