import pygame
import utils
import time

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
pantalla = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("HACKER RETRO v1.0")

# Carga de recursos
icono = utils.cargar_imagenes("hacker.png")
inicio = utils.cargar_imagenes("Inicio.jpg")
start = utils.cargar_imagenes('glitch-animation.gif')
pygame.display.set_icon(icono)
musica = utils.cargar_audio("musica-Juego.ogg")
if musica:
    musica.set_volume(0.1)
sonido_tecla= utils.cargar_efecto("una-sola-tecla.ogg")

# Configuración del menú
opciones = ['Iniciar Juego', 'Opciones', 'Salir']
indiceSeleccionado = 0
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
NEGRO = (0, 0, 0)

# Fuentes
fuente_base = "assets/fonts/Ac437_Acer_VGA_8x8.ttf"
fuenteTitulo = pygame.font.Font(fuente_base, 50)
fuenteOpcion = pygame.font.Font(fuente_base, 40)
fuenteEmail = pygame.font.Font(fuente_base, 15)  # Nueva fuente para emails
fuenteEmail2=pygame.font.Font(fuente_base,12)
# Estados del juego
estado = "intro"
intro_completada = False

# Variables para el sistema de emails
input_usuario = ""
comando_email = "abrir"
mostrando_emails = False
contenido_email = None
frase_inicial = "C:\\Users\\usuario>"
mostrar_cursor = int(time.time() * 2) % 2 == 0
mensajes = ["Cargando sistema...", "Estableciendo conexión...", "Autenticación exitosa."]

# Bucle principal
running = True
while running:
    eventos = pygame.event.get()  # Obtener eventos una sola vez por frame
    for event in eventos:
        if event.type == pygame.KEYDOWN and sonido_tecla:
            sonido_tecla.play()
        if event.type == pygame.QUIT:
            running = False

        # Manejo de eventos en el menú
        if estado == "menu":
            indiceSeleccionado = utils.manejar_eventos_menu(event, opciones, indiceSeleccionado)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if indiceSeleccionado == 0:
                    print("Iniciando juego...")
                    estado = "start"
                    # Resetear variables de email al entrar
                    input_usuario = ""
                    mostrando_emails = False
                    contenido_email = None
                elif indiceSeleccionado == 1:
                    print("Abriendo opciones...")
                elif indiceSeleccionado == 2:
                    running = False

    # Limpiar pantalla
    pantalla.fill(NEGRO)

    # Estados
    if estado == "intro":
        if not utils.efecto_inicio(pantalla, inicio, (0, 0), 1, 2):
            estado = "menu"

    elif estado == "menu":
        utils.dibujar_menu(pantalla, opciones, indiceSeleccionado, fuenteTitulo, fuenteOpcion, BLANCO, VERDE)
        if musica:
            musica.play()

    elif estado == "start":
        musica.stop()
        # Primero mostramos la pantalla para escribir el comando
        if not mostrando_emails:
            pantalla.fill(NEGRO)
            for event in eventos:
                resultado, input_usuario = utils.abrir_emails(
                    frase_inicial, 
                    comando_email, 
                    pantalla, 
                    fuenteEmail, 
                    VERDE, 
                    event, 
                    input_usuario
                )

                if resultado:  # Si el comando es correcto
                    mostrando_emails = True
                    # Cargamos el contenido del email
                    for i, msg in enumerate(mensajes):
                        texto = fuenteEmail.render(msg, True, VERDE)
                        pantalla.blit(texto, (50, 100 + i*20))
                        pygame.display.flip()
                        time.sleep(0.5)
                        contenido_email = utils.cargar_documento("emails", "01_anonymous_warning.txt")
            
            # Mostrar el prompt de entrada
            instruccion = fuenteEmail.render("Escribe 'abrir' y presiona Enter", True, BLANCO)
            pantalla.blit(instruccion, (10, 100))
            texto_renderizado = fuenteEmail.render(frase_inicial + input_usuario + ('_' if mostrar_cursor else ''), True, VERDE)
            pantalla.blit(texto_renderizado, (10, 180))
        
        # Si el comando fue correcto, mostramos el contenido del email
        else:
            if contenido_email:
                utils.mostrar_emails_en_pantalla(pantalla, fuenteEmail2, VERDE, contenido_email)
            else:
                error_msg = fuenteEmail.render("Error: No se pudo cargar el email", True, (255, 0, 0))
                pantalla.blit(error_msg, (50, 50))
            
            # Permitir volver al menú con ESC
            for event in eventos:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    estado = "menu"
                    mostrando_emails = False
                    input_usuario = ""

    pygame.display.flip()

# Salida del juego
pygame.quit()