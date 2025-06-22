import pygame

pygame.init() #con esta iniciacion ya tenemos todos los componentes de pygame a disposicion

pantalla= pygame.display.set_mode((800, 600)) #con esto establecemos el modo y tamaño que quiero para mi pantalla
                                    #los valores son en tuplas 
                                    
#todo lo que sucedad en una pantalla es un evento, sea desde cerrar la pantalla, hacer click, etc


#Configuracion de el TITULO E ICONO
#Titulo:
pygame.display.set_caption("Invasion Espacial")
#Icono:
icono=pygame.image.load("ovni.png")
pygame.display.set_icon(icono)


#Jugador 
img_jugador = pygame.image.load("cohete.png")
#posicion del jugador al iniciar
jugador_x=368
jugador_y=536

#Para poder arrojar nuestro jugador a la pantalla lo vamos a hacer con una funcion

def Jugador():
    #blit es el metodo que sig algo asi como arrojar 
    #se le pase la imagen y la tupla de donde se ubica
    pantalla.blit(img_jugador,(jugador_x, jugador_y))



se_ejecuta = True 

while se_ejecuta: #ingresamos a el ciclo while 

    #dentro del ciclo while llamamos a pantalla y le cambiamos el color con fill
    pantalla.fill((205,144,228))#los colores van en RGB y en una tupla

    for evento in pygame.event.get(): #buscamos los eventos que suceden en nuestra ventana
        if evento.type == pygame.QUIT: #cuando el evento sea QUIT que es la X de cerrar
            se_ejecuta=False #Salimos del ciclo while

    Jugador()

    #para poder ver los cambios de pantalla es necesario realizar una actualizacion del juego            
    pygame.display.update()