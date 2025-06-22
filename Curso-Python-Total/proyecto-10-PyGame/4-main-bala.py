import pygame
import random

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
enemigo_x_cambio = 0.1
enemigo_y_cambio = 50

#Variable de la balas 
img_bala = pygame.image.load("bala.png")
bala_x = 0
bala_y = 500 #dado que nuestra nave no se mueve verticalmente siempre va a salir de la misma altura
bala_y_cambio = 0.2 #velocidad de la bala
bala_visible= False #para que al principio no se vea la bala 


def Jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

def Enemigo(x, y):
    pantalla.blit(img_enemigo, (x, y))

#Funcion para disparar la bala
#la funcion principal es que disminuya su valor Y para que genere la ilucion de movimiento
def disparar_bala(x,y):
    global bala_visible #la hacemos global para que cuando se modifique dentro de la funcion se modifique la variable real y no solo dentro de la funcion
#para decirle a Python que no cree una nueva variable local, sino que quieres trabajar con la global → por eso usas global bala_visible
    bala_visible=True
    pantalla.blit(img_bala,(x+16,y+10)) #se les agrega un nro para que no aparezcan del costado de la nave sino del centro 



se_ejecuta = True

while se_ejecuta:
    pantalla.blit(fondo, (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -0.2
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.2
#Agregamos un evento mas para que cuando se aprete el ESPACIO dispare PEEERO SOLO SE DISPARE SI ESTA ES FALSA PORQUE SI ES VERDADERA SIGNIFICA QUE ESTA EN PANTALLA
            if evento.key == pygame.K_SPACE and bala_visible== False:
                bala_x=jugador_x
#esto se hacce para que la bala no siga a la nave y que una vez que se dispare siga su curso dado que ahora la direccion horizontal la determina bala_X
                disparar_bala(bala_x,bala_y) #con esto dejamos en claro que queremos que la bala salga del centro de nuestra nave 

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    if enemigo_x <= 0:
        enemigo_x_cambio = 0.1
        enemigo_y += enemigo_y_cambio
    elif enemigo_x >= 736:
        enemigo_x_cambio = -0.1
        enemigo_y += enemigo_y_cambio

#RANGO DE VISIBILIDAD DE LA BALA - -64 es para que desaparezca completamente de nuestra vista dado que la imagen tiene 64px
    if bala_y<=-64:
#una vez que se vaya de la pantalla vuelve a los valores por defecto que tenia en su inicio
        bala_y=500
        bala_visible=False


#MOVIMIENTO DE LA BALA PORQUE SINO APARECE Y SE QUEDA QUIETA
    if bala_visible: #si es true funciona
        disparar_bala(bala_x,bala_y)
        bala_y-=bala_y_cambio
#vamos restando esta vez para que bala_y vaya moviendose mientras avanza el bucle while


    enemigo_x += enemigo_x_cambio
    jugador_x += jugador_x_cambio

    Jugador(jugador_x, jugador_y)
    Enemigo(enemigo_x, enemigo_y)
    pygame.display.update()
