import pygame

pygame.init()

pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Invasion Espacial")
icono = pygame.image.load("ovni.png")
pygame.display.set_icon(icono)

img_jugador = pygame.image.load("cohete.png")
jugador_x = 368
jugador_y = 536
jugador_x_cambio = 0

def Jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

se_ejecuta = True

while se_ejecuta:
    pantalla.fill((205, 144, 228))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -0.1
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.1

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    #mantener dentro del cuadro
    if jugador_x<=0:
        jugador_x=0
    elif jugador_x>=736:
        jugador_x=736


    jugador_x += jugador_x_cambio
    Jugador(jugador_x, jugador_y)
    pygame.display.update()
