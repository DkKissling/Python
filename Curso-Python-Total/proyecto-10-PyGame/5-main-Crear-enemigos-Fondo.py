import pygame

#IMPORTAMOS RANDOM PARA QUE NUESTROS ENEMIGOS APAREZCAN DE FORMA ALETORIA
import random
pygame.init()

pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Invasion Espacial")
icono = pygame.image.load("ovni.png")
pygame.display.set_icon(icono)

#Imagen de fondo
fondo = pygame.image.load("fondo.jpg")

img_jugador = pygame.image.load("cohete.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

#Variables de enemigos
img_enemigo = pygame.image.load("enemigo.png")
enemigo_x = random.randint(0,736) #usamos randit para establecer el rango que queremos que tenga en ambos ejes
enemigo_y = random.randint(50,200)
enemigo_x_cambio = 0.1 #cambiamos la tasa de cambio para que se mueva siempre de izquierda a derecha
enemigo_y_cambio = 50 # vamos bajando nuestros enemigos para que se acerque a nuestra nave

def Jugador(x, y):
    pantalla.blit(img_jugador, (x, y))


#funcion enemigos
def Enemigo(x, y):
    pantalla.blit(img_enemigo, (x, y))


se_ejecuta = True

while se_ejecuta:

    #CAMBIAMOS EL METODO FILL POR BLIT PARA QUE TOME LA IMAGEN
    pantalla.blit(fondo,(0,0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -0.2
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.2

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0
    if jugador_x<=0:
        jugador_x=0
    elif jugador_x>=736:
        jugador_x=736
#MANTENER Y MODIFICAR UBICACION DEL ENEMIGO CUANDO LLEGUE A UN BORDE
    if enemigo_x<=0:
        enemigo_x_cambio=0.1
        enemigo_y+=enemigo_y_cambio
    elif enemigo_x>=736:
        enemigo_x_cambio=-0.1
        enemigo_y+=enemigo_y_cambio

#LA MISMA FUNCION DE JUGADOR 
    enemigo_x += enemigo_x_cambio


    jugador_x += jugador_x_cambio
    Jugador(jugador_x, jugador_y)
    Enemigo(enemigo_x,enemigo_y)
    pygame.display.update()
