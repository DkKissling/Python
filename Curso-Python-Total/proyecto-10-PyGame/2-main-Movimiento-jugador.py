import pygame

pygame.init()

pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Invasion Espacial")
icono = pygame.image.load("ovni.png")
pygame.display.set_icon(icono)

img_jugador = pygame.image.load("cohete.png")

#variables del jugador
jugador_x = 368
jugador_y = 536
#Agregamos una nueva variable con el valor de la modificacion de cada eje
jugador_x_cambio= 0



#Para ponerle movimiento hay que darle valores a la funcion Jugador
def Jugador(x,y):
    pantalla.blit(img_jugador, (x,y))

se_ejecuta = True

while se_ejecuta:
    pantalla.fill((205, 144, 228))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False
#para ver si se presiono una tecla usamos Keydown que toma todas las teclas
#vale aclarar que KEYDOWN eventos solo son cuando se presiona no cuando se levanta
        if evento.type == pygame.KEYDOWN:
        #K_LEFT Es la flecha izquierda y K_RIGHT derecha
            if evento.key == pygame.K_LEFT:
                #asi modificar 
                jugador_x_cambio=-0.1
                print("flecha izquierda")
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio=0.1
                print("flecha Derecha")
#Para saber cuando se levanta necesitamos otro evento
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                print("la tecla fue soltada ")
                jugador_x_cambio=0
  
    #sumamos sea cual sea el valor de jugador cambio a jugador x para que se mueva
    jugador_x += jugador_x_cambio
    Jugador(jugador_x,jugador_y)
    pygame.display.update()
