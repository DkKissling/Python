
#usamos una formula para calcular D =[√(X2-X1)2 - (Y2-Y1)2] 
#LAS COORDENADA OBJETO1 = X e Y - OBJETO2= X e Y

import pygame
import random
#Import math
import math


pygame.init()

pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Invasion Espacial")
icono = pygame.image.load("ovni.png")
pygame.display.set_icon(icono)

fondo = pygame.image.load("fondo.jpg")

img_jugador = pygame.image.load("cohete.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

img_enemigo = pygame.image.load("enemigo.png")
enemigo_x = random.randint(0, 736)
enemigo_y = random.randint(50, 200)
enemigo_x_cambio = 0.2
enemigo_y_cambio = 25

img_bala = pygame.image.load("bala.png")
bala_x = 0
bala_y = 500
bala_y_cambio = 2
bala_visible = False

#Puntaje para saber ir sumando puntos:
puntaje= 0

def Jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

def Enemigo(x, y):
    pantalla.blit(img_enemigo, (x, y))

def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))

#FORMULA PARA CALCULAR LAS COLISION VA A EXAMINAR SIEMPRE SI HAY UNA COLISION 
def hay_colision(x_1,y_1,x_2,y_2):
#sqrt es para la raiz cuadrada y pow para elevar al cuadrado (operacion y nro-elevado)
    distancia = math.sqrt(math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        False


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
            if evento.key == pygame.K_SPACE and bala_visible == False:
                bala_x = jugador_x
                disparar_bala(bala_x, bala_y)

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    if enemigo_x <= 0:
        enemigo_x_cambio = 0.2
        enemigo_y += enemigo_y_cambio
    elif enemigo_x >= 736:
        enemigo_x_cambio = -0.2
        enemigo_y += enemigo_y_cambio

    if bala_y <= -64:
        bala_y = 500
        bala_visible = False

    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio

#LLAMAMOS A LA FUNCION Y PASAMOS LA UBICACION DE CADA UNO DE LOS OBJETOS
    colision = hay_colision(enemigo_x,enemigo_y,bala_x,bala_y)
    if colision: #Si es verdadera la bala vuelve a la posicion original de false y 500 
        bala_y=500
        bala_visible=False
        puntaje+=1
#Reninciamos al enemigo para que desaparezca
        enemigo_x = random.randint(0, 736) 
        enemigo_y = random.randint(50, 200)

    enemigo_x += enemigo_x_cambio
    jugador_x += jugador_x_cambio

    Jugador(jugador_x, jugador_y)
    Enemigo(enemigo_x, enemigo_y)
    pygame.display.update()
