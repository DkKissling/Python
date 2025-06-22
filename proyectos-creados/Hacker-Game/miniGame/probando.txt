import pygame
import sys
import json
import random
import time
import os
import re

# ======================
# Configuración general
# ======================
WIDTH = 1000
HEIGHT = 800
FPS = 60

# Colores estilo retro terminal
NEGRO = (0, 0, 0)
VERDE_TERMINAL = (0, 255, 0)
VERDE_OSCURO = (0, 180, 0)
VERDE_CLARO = (150, 255, 150)
ROJO_TERMINAL = (255, 60, 60)
AZUL_TERMINAL = (0, 200, 255)
GRIS_TERMINAL = (80, 100, 80)
AMARILLO_TERMINAL = (255, 255, 0)

# Estados de juego
START_MENU, TERMINAL_LOGIN, TERMINAL_COMMAND, EMAIL_VIEWER = range(4)
BRUTE_FORCE, BINARY_CRACK, CIPHER_SPRINT, VICTORY, EXIT = range(4, 9)

# ======================
# Narrativa del juego
# ======================
HISTORIA = {
    "intro": "Año 2055. Eres un agente de ciberseguridad. Has detectado una intrusión en el sistema central. Debes navegar por el sistema para detener al hacker antes de que robe información confidencial.",
    "brute_force": "ALERTA: Se requiere la contraseña de administrador para continuar. El sistema de fuerza bruta ha sido activado.",
    "binary_crack": "ALERTA: Cortafuegos detectado. Necesitas descifrar los códigos binarios para eludir la seguridad.",
    "cipher_sprint": "ALERTA: Múltiples conexiones detectadas. Intercepta y escribe rápidamente las palabras clave para bloquear al intruso.",
    "victoria": "CONEXIÓN SEGURA ESTABLECIDA. Amenaza neutralizada. Sistema asegurado."
}

# Direcciones IP y comandos
SISTEMA_IPS = {
    "login": "192.168.1.1",
    "mainframe": "10.0.3.55",
    "security": "172.16.254.1",
    "final": "192.168.7.1"
}

COMANDOS_VALIDOS = [
    "connect", "ssh", "access", "scan", "run", "exec", "sudo", "help", "clear", "ls", "cd", "cat"
]

# ======================
# Funciones de utilidades
# ======================

def cargar_json_seguro(ruta):
    # Intentar primero con la ruta relativa directa
    if os.path.exists(ruta):
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # Si no funciona, intentar con el método anterior
    base = os.path.dirname(os.path.abspath(__file__))
    ruta_completa = os.path.normpath(os.path.join(base, os.pardir, ruta))
    
    if not os.path.exists(ruta_completa):
        # Si aún no funciona, intentar una tercera opción: mismo directorio
        ruta_alt = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.basename(ruta))
        if not os.path.exists(ruta_alt):
            # También intentar buscar en un directorio 'docs' en el mismo nivel
            ruta_docs = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs', os.path.basename(ruta))
            if not os.path.exists(ruta_docs):
                raise FileNotFoundError(f"No se encontró el archivo JSON en ninguna ubicación: {ruta}, {ruta_completa}, {ruta_alt}, {ruta_docs}")
            else:
                ruta_completa = ruta_docs
        else:
            ruta_completa = ruta_alt
    
    with open(ruta_completa, 'r', encoding='utf-8') as f:
        return json.load(f)

# Función para mostrar texto con efecto de máquina de escribir
def efecto_maquina_escribir(screen, texto, x, y, font, color=VERDE_TERMINAL, velocidad=3):
    texto_actual = ""
    for char in texto:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Permitir saltarse la animación con Enter
                return texto
                
        texto_actual += char
        screen.fill(NEGRO, (x, y, WIDTH-50, font.get_height()))
        text_surface = font.render(texto_actual, True, color)
        screen.blit(text_surface, (x, y))
        pygame.display.flip()
        pygame.time.delay(1000 // velocidad // 10)
    
    return texto

def mostrar_texto(screen, texto, x, y, font, color=VERDE_TERMINAL):
    img = font.render(texto, True, color)
    screen.blit(img, (x, y))

def mostrar_texto_con_saltos(screen, texto, x, y, font, max_width=700, line_height=35, color=VERDE_TERMINAL):
    """Muestra texto con saltos de línea automáticos cuando excede el ancho máximo"""
    palabras = texto.split()
    lineas = []
    linea_actual = ""
    
    for palabra in palabras:
        prueba = linea_actual + " " + palabra if linea_actual else palabra
        texto_prueba = font.render(prueba, True, color)
        
        if texto_prueba.get_width() <= max_width:
            linea_actual = prueba
        else:
            lineas.append(linea_actual)
            linea_actual = palabra
            
    if linea_actual:
        lineas.append(linea_actual)
        
    for i, linea in enumerate(lineas):
        img = font.render(linea, True, color)
        screen.blit(img, (x, y + i * line_height))
    
    return len(lineas) * line_height  # Devuelve la altura total utilizada

def dibujar_boton_terminal(screen, texto, x, y, w, h, color_inactivo, color_activo, font, accion=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(screen, color_activo, (x, y, w, h), 2)
        if click[0] == 1 and accion is not None:
            return accion
    else:
        pygame.draw.rect(screen, color_inactivo, (x, y, w, h), 2)
        
    text_surf = font.render(texto, True, color_inactivo)
    text_rect = text_surf.get_rect(center=((x + w/2), (y + h/2)))
    screen.blit(text_surf, text_rect)
    return None

# ======================
# Nueva función: Terminal de texto
# ======================
def terminal_text_input(screen, prompt, font, y_pos, input_text="", color=VERDE_TERMINAL, cursor_visible=True):
    # Dibujar el prompt
    prompt_surface = font.render(prompt, True, color)
    screen.blit(prompt_surface, (20, y_pos))
    
    # Dibujar el texto de entrada con un cursor parpadeante
    input_surface = font.render(input_text, True, color)
    screen.blit(input_surface, (20 + prompt_surface.get_width(), y_pos))
    
    # Dibujar el cursor si es visible
    if cursor_visible:
        cursor_x = 20 + prompt_surface.get_width() + input_surface.get_width() + 2
        pygame.draw.line(screen, color, 
                         (cursor_x, y_pos), 
                         (cursor_x, y_pos + font.get_height()), 2)
    
    return 20, y_pos + font.get_height() + 5  # Retorna la posición para la siguiente línea

# Función para dibujar el efecto de líneas de fondo tipo Matrix
def dibujar_efecto_matrix(screen, tiempo):
    # Crea rayas verticales aleatorias de código matriz
    num_lineas = 10
    for i in range(num_lineas):
        x = random.randint(0, WIDTH)
        longitud = random.randint(5, 30)
        velocidad = random.randint(1, 5)
        color_intensidad = random.randint(30, 100)
        
        y_start = (tiempo * velocidad) % (HEIGHT + longitud) - longitud
        
        for j in range(longitud):
            y = (y_start + j) % HEIGHT
            if 0 <= y < HEIGHT:
                color = (0, color_intensidad, 0)
                pygame.draw.line(screen, color, (x, y), (x, y+1), 1)

# ======================
# Terminal para ingresar comandos
# ======================
def terminal_comandos(screen, font, pequeño_font, nivel_objetivo):
    historial = []
    historial.append("$ SISTEMA INICIADO")
    historial.append("$ ESPERANDO COMANDOS...")
    historial.append(f"$ Objetivo actual: {nivel_objetivo}")
    
    # Definir qué comandos específicos se necesitan según el nivel
    if nivel_objetivo == BRUTE_FORCE:
        comando_correcto = f"connect {SISTEMA_IPS['mainframe']} -u admin"
        ip_mostrar = SISTEMA_IPS['mainframe']
        mensaje_ayuda = f"AYUDA: Usa 'connect [IP] -u [usuario]' para acceder al sistema. IP objetivo: {ip_mostrar}"
    elif nivel_objetivo == BINARY_CRACK:
        comando_correcto = f"sudo access {SISTEMA_IPS['security']} --bypass"
        ip_mostrar = SISTEMA_IPS['security']
        mensaje_ayuda = f"AYUDA: Usa 'sudo access [IP] --bypass' para eludir el cortafuegos. IP objetivo: {ip_mostrar}"
    elif nivel_objetivo == CIPHER_SPRINT:
        comando_correcto = f"run CHAOS.EXE {SISTEMA_IPS['final']}"
        ip_mostrar = SISTEMA_IPS['final']
        mensaje_ayuda = f"AYUDA: Usa 'run CHAOS.EXE [IP]' para ejecutar el programa de bloqueo. IP objetivo: {ip_mostrar}"
    else:
        comando_correcto = "help"
        ip_mostrar = "DESCONOCIDO"
        mensaje_ayuda = "AYUDA: Usa 'help' para mostrar comandos disponibles."
    
    input_text = ""
    cursor_visible = True
    timer = 0
    cursor_timer = 0
    
    clock = pygame.time.Clock()
    
    while True:
        tiempo_actual = pygame.time.get_ticks() / 1000  # Tiempo en segundos
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return EXIT
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    if input_text.strip().lower() == "help":
                        historial.append(f"$ {input_text}")
                        historial.append("  COMANDOS DISPONIBLES:")
                        historial.append("  connect [IP] -u [usuario] : Conectar a un sistema")
                        historial.append("  access [IP] --bypass      : Intentar acceso privilegiado")
                        historial.append("  run [PROGRAMA] [DESTINO]  : Ejecutar un programa")
                        historial.append("  clear                     : Limpiar pantalla")
                        historial.append("  ls                        : Listar archivos")
                        historial.append(mensaje_ayuda)
                        input_text = ""
                    elif input_text.strip().lower() == "clear":
                        historial = []
                        historial.append("$ PANTALLA LIMPIA")
                        historial.append(f"$ Objetivo actual: {nivel_objetivo}")
                        input_text = ""
                    elif input_text.strip().lower() == "ls":
                        historial.append(f"$ {input_text}")
                        historial.append("  system.log")
                        historial.append("  CHAOS.EXE")
                        historial.append("  access_codes.bin")
                        historial.append("  emails/")
                        input_text = ""
                    elif re.match(r"cat\s+emails?", input_text.strip().lower()):
                        historial.append(f"$ {input_text}")
                        historial.append("  Mostrando contenido del directorio emails/...")
                        historial.append("  01_anonymous_warning.txt")
                        historial.append("  02_nexus_internal.txt")
                        historial.append("  03_scientist_confession.txt")
                        historial.append("  Para leer un email, usa 'cat emails/[nombre_archivo]'")
                        input_text = ""
                    elif input_text.strip().lower().startswith("cat emails/"):
                        historial.append(f"$ {input_text}")
                        historial.append("  Abriendo visualizador de emails...")
                        pygame.time.delay(500)
                        email_num = input_text.strip().lower().replace("cat emails/", "").replace(".txt", "").replace("0", "")
                        if email_num in ["1", "2", "3"]:
                            index = int(email_num) - 1
                            return EMAIL_VIEWER, index
                        else:
                            historial.append("  ERROR: Archivo no encontrado")
                        input_text = ""
                    elif input_text.strip().lower() == comando_correcto:
                        historial.append(f"$ {input_text}")
                        historial.append("  CONECTANDO...")
                        historial.append(f"  ACCESO CONCEDIDO A {ip_mostrar}")
                        pygame.time.delay(1000)
                        return nivel_objetivo, None
                    else:
                        historial.append(f"$ {input_text}")
                        if any(cmd in input_text.lower() for cmd in COMANDOS_VALIDOS):
                            historial.append("  COMANDO INCORRECTO O PERMISOS INSUFICIENTES")
                        else:
                            historial.append("  COMANDO NO RECONOCIDO. Usa 'help' para ver comandos disponibles.")
                        input_text = ""
                elif e.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif e.key == pygame.K_ESCAPE:
                    return START_MENU, None
                elif e.unicode.isprintable():
                    input_text += e.unicode
                    
        screen.fill(NEGRO)
        
        # Dibujar fondo estilo matrix (sutil)
        dibujar_efecto_matrix(screen, tiempo_actual)
        
        # Dibujar el borde de la terminal
        pygame.draw.rect(screen, VERDE_TERMINAL, (10, 10, WIDTH-20, HEIGHT-20), 2)
        
        # Dibujar la barra superior de la terminal
        pygame.draw.rect(screen, VERDE_OSCURO, (10, 10, WIDTH-20, 30))
        mostrar_texto(screen, "SISTEMA DE SEGURIDAD - TERMINAL v3.55", WIDTH//2 - 180, 18, pequeño_font)
        
        # Mostrar historial de comandos
        y_offset = 50
        for linea in historial[-15:]:  # Mostrar solo las últimas 15 líneas
            mostrar_texto(screen, linea, 20, y_offset, pequeño_font)
            y_offset += 25
            
        # Cursor parpadeante cada 0.5 segundos
        cursor_timer += 1
        if cursor_timer > FPS / 2:
            cursor_visible = not cursor_visible
            cursor_timer = 0
            
        # Input de texto actual
        terminal_text_input(screen, "$ ", font, HEIGHT - 60, input_text, VERDE_TERMINAL, cursor_visible)
        
        pygame.display.flip()
        clock.tick(FPS)

# ======================
# Visualizador de emails
# ======================
def email_viewer(screen, font, small_font, email_index):
    try:
        emails_data = cargar_json_seguro("emails.json")
        email = emails_data["archivos"][email_index]
    except (FileNotFoundError, IndexError) as e:
        print(f"Error al cargar el email: {e}")
        email = {
            "nombre": "ERROR.txt",
            "origen": "SISTEMA",
            "destinatario": "USUARIO",
            "asunto": "ERROR DE CARGA",
            "contenido": "No se pudo cargar el email solicitado. El archivo puede estar corrupto o no existir."
        }
        
    clock = pygame.time.Clock()
    scrollY = 0
    max_scroll = 0  # Se actualizará después de renderizar el contenido
    
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return EXIT
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE or e.key == pygame.K_RETURN:
                    return TERMINAL_COMMAND
                elif e.key == pygame.K_UP:
                    scrollY = max(0, scrollY - 20)
                elif e.key == pygame.K_DOWN:
                    scrollY = min(max_scroll, scrollY + 20)
                    
        screen.fill(NEGRO)
        
        # Dibujar interfaz de email estilo terminal retro
        pygame.draw.rect(screen, VERDE_TERMINAL, (10, 10, WIDTH-20, HEIGHT-20), 2)
        pygame.draw.rect(screen, VERDE_OSCURO, (10, 10, WIDTH-20, 30))
        mostrar_texto(screen, f"VISUALIZADOR DE EMAIL - {email['nombre']}", WIDTH//2 - 200, 18, small_font)
        
        # Contenido del email
        y_offset = 50 - scrollY
        
        # Encabezados
        mostrar_texto(screen, f"De: {email['origen']}", 20, y_offset, small_font, AMARILLO_TERMINAL)
        y_offset += 25
        mostrar_texto(screen, f"Para: {email['destinatario']}", 20, y_offset, small_font, AMARILLO_TERMINAL)
        y_offset += 25
        mostrar_texto(screen, f"Asunto: {email['asunto']}", 20, y_offset, small_font, AMARILLO_TERMINAL)
        y_offset += 35
        
        # Línea divisoria
        pygame.draw.line(screen, VERDE_TERMINAL, (20, y_offset), (WIDTH-20, y_offset), 1)
        y_offset += 20
        
        # Contenido con saltos de línea
        altura_contenido = mostrar_texto_con_saltos(screen, email['contenido'], 20, y_offset, small_font)
        y_offset += altura_contenido + 20
        
        # Calcular scroll máximo
        max_scroll = max(0, y_offset - HEIGHT + 50)
        
        # Instrucciones al pie
        pygame.draw.rect(screen, VERDE_OSCURO, (10, HEIGHT-40, WIDTH-20, 30))
        mostrar_texto(screen, "ESC o ENTER: Volver | ↑↓: Desplazar", WIDTH//2 - 180, HEIGHT-30, small_font)
        
        # Indicador de desplazamiento si es necesario
        if max_scroll > 0:
            # Calcula la posición y tamaño de la barra de desplazamiento
            scrollbar_height = (HEIGHT - 80) * min(1, HEIGHT / (y_offset + scrollY))
            scrollbar_pos = 50 + (HEIGHT - 140) * (scrollY / max_scroll)
            pygame.draw.rect(screen, VERDE_TERMINAL, (WIDTH-25, scrollbar_pos, 10, scrollbar_height))

        pygame.display.flip()
        clock.tick(FPS)

# ======================
# Pantalla de inicio estilo terminal
# ======================
def mostrar_inicio(screen, font, small_font):
    clock = pygame.time.Clock()
    
    # Líneas de introducción con efecto de terminal
    lineas_intro = [
        "INICIANDO SISTEMA DE SEGURIDAD...",
        "CARGANDO MÓDULOS...",
        "CONFIGURANDO FIREWALLS...",
        "ACTIVANDO PROTOCOLOS DE SEGURIDAD...",
        "SISTEMA LISTO."
    ]
    
    # Textos para el menú
    titulo = "CIBERMISIÓN: PROTEGE EL SISTEMA"
    subtitulo = "TERMINAL DE ACCESO SEGURO v3.55"
    
    # Animación de inicio
    screen.fill(NEGRO)
    y_pos = 50
    for linea in lineas_intro:
        efecto_maquina_escribir(screen, linea, 20, y_pos, small_font, VERDE_TERMINAL, 10)
        y_pos += 30
        pygame.time.delay(300)
    
    pygame.time.delay(500)
    
    anim_completada = False
    input_text = ""
    cursor_visible = True
    cursor_timer = 0
    mostrar_prompt = False
    tiempo_espera = 0
    
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return EXIT
            if e.type == pygame.KEYDOWN:
                if not anim_completada:
                    anim_completada = True
                elif mostrar_prompt:
                    if e.key == pygame.K_RETURN:
                        if input_text.lower() == "start" or input_text.lower() == "login":
                            return TERMINAL_LOGIN
                        elif input_text.lower() == "exit" or input_text.lower() == "quit":
                            return EXIT
                        else:
                            input_text = ""
                    elif e.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif e.unicode.isprintable():
                        input_text += e.unicode
                else:
                    mostrar_prompt = True
                    
        tiempo_actual = pygame.time.get_ticks() / 1000
        
        screen.fill(NEGRO)
        
        # Dibujar fondo estilo matrix (sutil)
        dibujar_efecto_matrix(screen, tiempo_actual)
        
        # Dibujar el borde de la terminal
        pygame.draw.rect(screen, VERDE_TERMINAL, (10, 10, WIDTH-20, HEIGHT-20), 2)
        
        # Dibujar la barra superior de la terminal
        pygame.draw.rect(screen, VERDE_OSCURO, (10, 10, WIDTH-20, 30))
        mostrar_texto(screen, subtitulo, WIDTH//2 - 180, 18, small_font)
        
        if anim_completada:
            # Mostrar título
            mostrar_texto(screen, titulo, WIDTH//2 - 250, 100, font, VERDE_TERMINAL)
            mostrar_texto(screen, "Una aventura hacker", WIDTH//2 - 100, 160, small_font, VERDE_CLARO)
            
            # Instrucciones
            mostrar_texto(screen, "Para iniciar la misión, escribe 'LOGIN' o 'START'", WIDTH//2 - 230, 250, small_font)
            mostrar_texto(screen, "Para salir, escribe 'EXIT'", WIDTH//2 - 130, 280, small_font)
            
            if not mostrar_prompt:
                tiempo_espera += 1
                if tiempo_espera > FPS * 2:  # Esperar 2 segundos
                    mostrar_prompt = True
            
            if mostrar_prompt:
                # Cursor parpadeante cada 0.5 segundos
                cursor_timer += 1
                if cursor_timer > FPS / 2:
                    cursor_visible = not cursor_visible
                    cursor_timer = 0
                
                # Prompt de comando
                terminal_text_input(screen, "> ", font, HEIGHT - 100, input_text, VERDE_TERMINAL, cursor_visible)
        else:
            # Mostrar líneas de inicio
            y_pos = 50
            for linea in lineas_intro:
                mostrar_texto(screen, linea, 20, y_pos, small_font)
                y_pos += 30
                
        pygame.display.flip()
        clock.tick(FPS)

# ======================
# Pantalla de login terminal
# ======================
def terminal_login(screen, font, small_font):
    clock = pygame.time.Clock()
    usuario = ""
    password = ""
    estado_input = "usuario"  # o "password"
    cursor_visible = True
    cursor_timer = 0
    mensaje_error = ""
    intentos = 0
    
    # Datos de login válidos
    login_valido = {"admin": "1234", "guest": "guest", "user": "password"}
    
    # Texto de la pantalla
    titulo = "SISTEMA DE SEGURIDAD CENTRAL"
    subtitulo = "LOGIN DE ACCESO"
    
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return EXIT
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return START_MENU
                elif e.key == pygame.K_RETURN:
                    if estado_input == "usuario":
                        if usuario.strip():
                            estado_input = "password"
                        else:
                            mensaje_error = "ERROR: Ingrese un nombre de usuario"
                    else:  # estado_input == "password"
                        if usuario in login_valido and password == login_valido[usuario]:
                            # Login exitoso
                            return TERMINAL_COMMAND
                        else:
                            intentos += 1
                            mensaje_error = f"ERROR: Credenciales incorrectas. Intento {intentos}/3"
                            password = ""
                            if intentos >= 3:
                                mensaje_error = "ERROR: Demasiados intentos fallidos. Reestableciendo..."
                                pygame.time.delay(1000)
                                return START_MENU
                elif e.key == pygame.K_BACKSPACE:
                    if estado_input == "usuario":
                        usuario = usuario[:-1]
                    else:
                        password = password[:-1]
                elif e.unicode.isprintable():
                    if estado_input == "usuario":
                        usuario += e.unicode
                    else:
                        password += e.unicode
                        
        # Tiempo actual para animaciones
        tiempo_actual = pygame.time.get_ticks() / 1000
                        
        screen.fill(NEGRO)
        
        # Dibujar fondo estilo matrix (sutil)
        dibujar_efecto_matrix(screen, tiempo_actual)
        
        # Dibujar el borde de la terminal
        pygame.draw.rect(screen, VERDE_TERMINAL, (10, 10, WIDTH-20, HEIGHT-20), 2)
        
        # Dibujar la barra superior de la terminal
        pygame.draw.rect(screen, VERDE_OSCURO, (10, 10, WIDTH-20, 30))
        mostrar_texto(screen, subtitulo, WIDTH//2 - 80, 18, small_font)
        
        # Mostrar título
        mostrar_texto(screen, titulo, WIDTH//2 - 200, 80, font, VERDE_TERMINAL)
        
        # Línea separadora
        pygame.draw.line(screen, VERDE_TERMINAL, (50, 130), (WIDTH-50, 130), 1)
        
        # Información de acceso
        mostrar_texto(screen, "Para continuar, ingrese sus credenciales de acceso.", 50, 160, small_font)
        mostrar_texto(screen, "El usuario y contraseña distinguen mayúsculas y minúsculas.", 50, 190, small_font)
        
        # Cursor parpadeante cada 0.5 segundos
        cursor_timer += 1
        if cursor_timer > FPS / 2:
            cursor_visible = not cursor_visible
            cursor_timer = 0
                
        # Inputs de usuario y password
        mostrar_texto(screen, "Usuario:", 50, 250, small_font)
        pygame.draw.rect(screen, VERDE_OSCURO, (170, 245, 300, 30), 1)
        mostrar_texto(screen, usuario, 180, 250, small_font)
        
        if estado_input == "usuario" and cursor_visible:
            cursor_x = 180 + small_font.size(usuario)[0]
            pygame.draw.line(screen, VERDE_TERMINAL, (cursor_x, 250), (cursor_x, 270), 2)
        
        mostrar_texto(screen, "Contraseña:", 50, 300, small_font)
        pygame.draw.rect(screen, VERDE_OSCURO, (170, 295, 300, 30), 1)
        mostrar_texto(screen, "*" * len(password), 180, 300, small_font)
        
        if estado_input == "password" and cursor_visible:
            cursor_x = 180 + small_font.size("*" * len(password))[0]
            pygame.draw.line(screen, VERDE_TERMINAL, (cursor_x, 300), (cursor_x, 320), 2)
            

            
    # Mensaje de error si existe
        if mensaje_error:
            mostrar_texto(screen, mensaje_error, 50, 350, small_font, ROJO_TERMINAL)
            
        # Información en pie de página
        pygame.draw.rect(screen, VERDE_OSCURO, (10, HEIGHT-40, WIDTH-20, 30))
        mostrar_texto(screen, "ESC: Volver | ENTER: Confirmar", WIDTH//2 - 150, HEIGHT-30, small_font)
    
        pygame.display.flip()
        clock.tick(FPS)

# ======================
# Mini-juegos adaptados al estilo terminal
# ======================

# Mini-juego 1: BruteForce con estilo terminal
def jugar_bruteforce(screen, font, small_font):
    try:
        data = cargar_json_seguro("palabras.json")
        palabra, pista = random.choice(list(data.items()))
    except (FileNotFoundError, json.JSONDecodeError):
        # Si no se encuentra el archivo, usar datos predefinidos
        palabras_backup = {
            "firewall": "Barrera de protección contra intrusos",
            "cifrado": "Proceso de transformar información para hacerla ilegible",
            "terminal": "Interfaz de comandos para interactuar con el sistema",
            "binario": "Sistema numérico de base 2",
            "backdoor": "Acceso secreto a un sistema"
        }
        palabra, pista = random.choice(list(palabras_backup.items()))
    
    letras_correctas = ['_' for _ in palabra]
    intento = ''
    errores = 0
    max_errores = 5
    terminado = False
    reloj = pygame.time.Clock()
    
    while True:
        tiempo_actual = pygame.time.get_ticks() / 1000
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return EXIT
            if not terminado and e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return TERMINAL_COMMAND
                elif e.key == pygame.K_RETURN:
                    if intento.lower() == palabra.lower():
                        letras_correctas = list(palabra)
                        terminado = True
                    else:
                        for i, c in enumerate(intento[:len(palabra)]):
                            if c.lower() == palabra[i].lower(): 
                                letras_correctas[i] = palabra[i]
                        errores += 1
                        if errores >= max_errores:
                            terminado = True
                        intento = ''
                elif e.key == pygame.K_BACKSPACE:
                    intento = intento[:-1]
                else:
                    if e.unicode.isalpha(): 
                        intento += e.unicode.lower()

        screen.fill(NEGRO)
        
        # Dibujar fondo estilo matrix (sutil)
        dibujar_efecto_matrix(screen, tiempo_actual)
        
        # Dibujar el borde de la terminal
        pygame.draw.rect(screen, VERDE_TERMINAL, (10, 10, WIDTH-20, HEIGHT-20), 2)
        
        # Dibujar la barra superior de la terminal
        pygame.draw.rect(screen, VERDE_OSCURO, (10, 10, WIDTH-20, 30))
        mostrar_texto(screen, "MÓDULO DE FUERZA BRUTA v2.1", WIDTH//2 - 180, 18, small_font)

        # Mostrar interfaz del juego de fuerza bruta
        mostrar_texto(screen, "SISTEMA DE DESCIFRADO DE CONTRASEÑAS", WIDTH//2 - 250, 60, font, VERDE_TERMINAL)
        mostrar_texto(screen, f"Pista: {pista}", 50, 120, small_font, AMARILLO_TERMINAL)
        mostrar_texto(screen, "Contraseña: " + ' '.join(letras_correctas), 50, 170, font, VERDE_TERMINAL)
        mostrar_texto(screen, f"Intento: {intento}", 50, 220, small_font, VERDE_CLARO)
        mostrar_texto(screen, f"Errores: {errores}/{max_errores}", 50, 270, small_font, 
                     ROJO_TERMINAL if errores > max_errores // 2 else VERDE_CLARO)

        # Barra de progreso de intentos
        pygame.draw.rect(screen, GRIS_TERMINAL, (50, 300, 300, 20))
        if max_errores > 0:
            barra_ancho = 300 * (1 - errores / max_errores)
            pygame.draw.rect(screen, VERDE_TERMINAL, (50, 300, max(0, barra_ancho), 20))

        if terminado:
            resultado = "✓ CONTRASEÑA DESCIFRADA" if ''.join(letras_correctas).lower() == palabra.lower() else f"✗ ACCESO DENEGADO. La contraseña era '{palabra}'"
            color = VERDE_TERMINAL if "✓" in resultado else ROJO_TERMINAL
            mostrar_texto(screen, resultado, 50, 350, font, color)
            
            # Pie de página con instrucciones
            pygame.draw.rect(screen, VERDE_OSCURO, (10, HEIGHT-40, WIDTH-20, 30))
            mostrar_texto(screen, "ENTER: Continuar", WIDTH//2 - 80, HEIGHT-30, small_font)
            
            pygame.display.flip()
            
            # Esperar a que presionen Enter
            esperar = True
            while esperar:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        return EXIT
                    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                        esperar = False
                        
            if "✓" in resultado:
                return BINARY_CRACK, None
            else:
                return TERMINAL_COMMAND, None
        
        # Pie de página con instrucciones
        pygame.draw.rect(screen, VERDE_OSCURO, (10, HEIGHT-40, WIDTH-20, 30))
        mostrar_texto(screen, "ESC: Abortar | ENTER: Verificar", WIDTH//2 - 150, HEIGHT-30, small_font)
        
        pygame.display.flip()
        reloj.tick(FPS)

# Mini-juego 2: Binary Crack con estema terminal
def jugar_binary_crack(screen, font, small_font):
    codes = [("01001000", "H"), ("01100001", "a"), ("01100011", "c"), 
             ("01101011", "k"), ("01100101", "e"), ("01110010", "r")]
    binary_dict = {chr(i): format(i, '08b') for i in range(65, 91)}  # A-Z
    binary_dict.update({chr(i): format(i, '08b') for i in range(97, 123)})  # a-z
    
    current = 0
    input_text = ''
    attempts = 3
    show_help = False
    reloj = pygame.time.Clock()

    while True:
        tiempo_actual = pygame.time.get_ticks() / 1000
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return EXIT
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return TERMINAL_COMMAND
                elif e.key == pygame.K_TAB:
                    show_help = not show_help
                elif e.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif e.key == pygame.K_RETURN:
                    if input_text.strip().upper() == codes[current][1].upper():
                        current += 1
                        input_text = ''
                        attempts = 3
                        if current >= len(codes):
                            # Mostrar palabra completa antes de continuar
                            screen.fill(NEGRO)
                            dibujar_efecto_matrix(screen, tiempo_actual)
                            pygame.draw.rect(screen, VERDE_TERMINAL, (10, 10, WIDTH-20, HEIGHT-20), 2)
                            pygame.draw.rect(screen, VERDE_OSCURO, (10, 10, WIDTH-20, 30))
                            mostrar_texto(screen, "MÓDULO DE DESCIFRADO BINARIO - COMPLETADO", WIDTH//2 - 250, 18, small_font)
                            
                            palabra_completa = ''.join([code[1] for code in codes])
                            mostrar_texto(screen, f"DESCIFRADO EXITOSO", WIDTH//2 - 120, 100, font, VERDE_TERMINAL)
                            mostrar_texto(screen, f'Palabra descifrada: "{palabra_completa}"', WIDTH//2 - 180, 180, font, VERDE_CLARO)
                            mostrar_texto(screen, 'Cargando siguiente módulo...', WIDTH//2 - 150, 260, small_font, AMARILLO_TERMINAL)
                            
                            # Barra de progreso
                            pygame.draw.rect(screen, GRIS_TERMINAL, (WIDTH//2 - 150, 300, 300, 20))
                            for i in range(30):
                                pygame.draw.rect(screen, VERDE_TERMINAL, (WIDTH//2 - 150, 300, i*10, 20))
                                pygame.display.flip()
                                pygame.time.delay(50)
                            
                            return CIPHER_SPRINT, None
                    else:
                        attempts -= 1
                        input_text = ''
                        if attempts <= 0:
                            return TERMINAL_COMMAND, None
                else:
                    input_text += e.unicode

        screen.fill(NEGRO)
        dibujar_efecto_matrix(screen, tiempo_actual)
        pygame.draw.rect(screen, VERDE_TERMINAL, (10, 10, WIDTH-20, HEIGHT-20), 2)
        pygame.draw.rect(screen, VERDE_OSCURO, (10, 10, WIDTH-20, 30))
        mostrar_texto(screen, "MÓDULO DE DESCIFRADO BINARIO v1.2", WIDTH//2 - 200, 18, small_font)
        
        mostrar_texto(screen, "DECODIFICADOR DE CORTAFUEGOS", WIDTH//2 - 200, 60, font, VERDE_TERMINAL)
        mostrar_texto(screen, f"CÓDIGO {current+1}/{len(codes)}: {codes[current][0]}", 50, 120, font, VERDE_TERMINAL)
        mostrar_texto(screen, f"Respuesta: {input_text}", 50, 180, small_font, VERDE_CLARO)
        mostrar_texto(screen, f"Intentos restantes: {attempts}", 50, 230, small_font, 
                      ROJO_TERMINAL if attempts == 1 else AMARILLO_TERMINAL)
        mostrar_texto(screen, "Presiona TAB para tabla de referencia", 50, 270, small_font, AZUL_TERMINAL)

        # Progreso
        mostrar_texto(screen, "Progreso:", 50, 310, small_font)
        palabra_actual = ''.join([codes[i][1] if i < current else "_" for i in range(len(codes))])
        mostrar_texto(screen, palabra_actual, 150, 310, small_font, VERDE_TERMINAL)

        if show_help:
            # Fondo oscurecido para la tabla
            pygame.draw.rect(screen, (0, 0, 0, 128), (40, 350, WIDTH-80, 200))
            pygame.draw.rect(screen, VERDE_TERMINAL, (40, 350, WIDTH-80, 200), 2)
            
            # Mostrar tabla de ayuda en formato de cuadrícula
            y0 = 360
            filas = 4
            cols = 7
            w_celda = 100
            h_celda = 35
            mostrar_texto(screen, 'Tabla ASCII-Binario:', 50, y0, small_font, AMARILLO_TERMINAL)
            
            items = list(binary_dict.items())[:26]  # Solo las letras que necesitamos
            for i, (k, v) in enumerate(items):
                fila = i // cols
                col = i % cols
                x = 50 + col * w_celda
                y = y0 + 30 + fila * h_celda
                pygame.draw.rect(screen, VERDE_OSCURO, (x, y, w_celda-5, h_celda-5), 1)
                mostrar_texto(screen, f'{k}: {v}', x+5, y+5, small_font, VERDE_CLARO)

        # Pie de página con instrucciones
        pygame.draw.rect(screen, VERDE_OSCURO, (10, HEIGHT-40, WIDTH-20, 30))
        mostrar_texto(screen, "ESC: Abortar | ENTER: Verificar | TAB: Ayuda", WIDTH//2 - 220, HEIGHT-30, small_font)
        
        pygame.display.flip()
        reloj.tick(FPS)

# Mini-juego 3: Cipher Sprint con estilo terminal
def jugar_cipher_sprint(screen, font, small_font):
    try:    
        data = cargar_json_seguro("confidencial.json")
        frases = data.get('mensajes_confidenciales', [])
        if not frases:
            raise FileNotFoundError
    except (FileNotFoundError, json.JSONDecodeError):
        # Frases predefinidas si no se encuentra el archivo
        frases = [
            "El acceso a la información confidencial ha sido bloqueado exitosamente.",
            "Los protocolos de seguridad han sido restablecidos en todos los servidores.",
            "El intruso ha sido detectado y eliminado del sistema central.",
            "Todos los archivos sensibles están ahora protegidos con cifrado de nivel militar.",
            "El cortafuegos ha sido actualizado para prevenir futuros intentos de intrusión."
        ]
    
    frase = random.choice(frases)
    palabras = list(set(frase.replace('.', '').replace(',', '').split()))
    a_tipear = random.sample(palabras, min(5, len(palabras)))
    idx, text_in = 0, ''
    intentos, tiempo_lim = 5, 60
    start = time.time()
    reloj = pygame.time.Clock()

    while True:
        tiempo_actual = pygame.time.get_ticks() / 1000
        elapsed = time.time() - start
        remaining = max(0, tiempo_lim - elapsed)
        
        # Verificar condiciones de fin de juego
        if remaining <= 0:
            resultado = '¡TIEMPO AGOTADO!'
            break
        elif intentos <= 0:
            resultado = '¡INTENTOS AGOTADOS!'
            break
        elif idx >= len(a_tipear):
            resultado = '¡INTERCEPTACIÓN COMPLETA!'
            break

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return EXIT
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return TERMINAL_COMMAND
                elif e.key == pygame.K_BACKSPACE:
                    text_in = text_in[:-1]
                elif e.key == pygame.K_RETURN:
                    if text_in.strip().lower() == a_tipear[idx].lower():
                        idx += 1
                    else:
                        intentos -= 1
                    text_in = ''
                else:
                    text_in += e.unicode

        screen.fill(NEGRO)
        dibujar_efecto_matrix(screen, tiempo_actual)
        pygame.draw.rect(screen, VERDE_TERMINAL, (10, 10, WIDTH-20, HEIGHT-20), 2)
        pygame.draw.rect(screen, VERDE_OSCURO, (10, 10, WIDTH-20, 30))
        mostrar_texto(screen, "MÓDULO DE INTERCEPTACIÓN v3.0", WIDTH//2 - 180, 18, small_font)
        
        mostrar_texto(screen, "INTERCEPTOR DE COMUNICACIONES", WIDTH//2 - 200, 60, font, VERDE_TERMINAL)
        mostrar_texto(screen, "Tipee las palabras clave interceptadas:", 50, 110, small_font, AMARILLO_TERMINAL)
        
        # Mostrar progreso de palabras
        progreso = f"Progreso: {idx}/{len(a_tipear)} palabras"
        mostrar_texto(screen, progreso, 50, 150, font, VERDE_TERMINAL)
        
        # Sólo mostramos la palabra actual si todavía quedan palabras por tipear
        if idx < len(a_tipear):
            mostrar_texto(screen, f'Objetivo: {a_tipear[idx]}', 50, 200, font, AZUL_TERMINAL)
        else:
            mostrar_texto(screen, '¡Secuencia completa!', 50, 200, font, VERDE_TERMINAL)
            
        mostrar_texto(screen, f'Entrada: {text_in}', 50, 250, font, VERDE_CLARO)
        mostrar_texto(screen, f'Intentos: {intentos}', 50, 300, font, 
                      ROJO_TERMINAL if intentos <= 2 else AMARILLO_TERMINAL)
        
        # Barra de tiempo
        mostrar_texto(screen, f'Tiempo: {int(remaining)}s', 50, 340, small_font, AMARILLO_TERMINAL)
        tiempo_porcentaje = remaining / tiempo_lim
        ancho_barra = int(700 * tiempo_porcentaje)
        pygame.draw.rect(screen, GRIS_TERMINAL, (50, 370, 700, 20))
        color_barra = VERDE_TERMINAL if tiempo_porcentaje > 0.3 else ROJO_TERMINAL
        pygame.draw.rect(screen, color_barra, (50, 370, ancho_barra, 20))
        
        # Pie de página con instrucciones
        pygame.draw.rect(screen, VERDE_OSCURO, (10, HEIGHT-40, WIDTH-20, 30))
        mostrar_texto(screen, "ESC: Abortar | ENTER: Verificar", WIDTH//2 - 150, HEIGHT-30, small_font)
        
        pygame.display.flip()
        reloj.tick(FPS)

    # Pantalla de resultado
    screen.fill(NEGRO)
    dibujar_efecto_matrix(screen, tiempo_actual)
    pygame.draw.rect(screen, VERDE_TERMINAL, (10, 10, WIDTH-20, HEIGHT-20), 2)
    pygame.draw.rect(screen, VERDE_OSCURO, (10, 10, WIDTH-20, 30))
    
    if 'COMPLETA' in resultado:
        mostrar_texto(screen, "MÓDULO DE INTERCEPTACIÓN - ÉXITO", WIDTH//2 - 230, 18, small_font)
        mostrar_texto(screen, resultado, WIDTH//2 - 150, 100, font, VERDE_TERMINAL)
        mostrar_texto(screen, 'Mensaje desbloqueado:', 50, 180, small_font, AMARILLO_TERMINAL)
        mostrar_texto_con_saltos(screen, frase, 50, 220, small_font, color=VERDE_CLARO)
    else:
        mostrar_texto(screen, "MÓDULO DE INTERCEPTACIÓN - FALLIDO", WIDTH//2 - 230, 18, small_font)
        mostrar_texto(screen, resultado, WIDTH//2 - 150, 100, font, ROJO_TERMINAL)
        mostrar_texto(screen, 'No se pudo interceptar el mensaje.', 50, 180, small_font, ROJO_TERMINAL)
    
    # Pie de página
    pygame.draw.rect(screen, VERDE_OSCURO, (10, HEIGHT-40, WIDTH-20, 30))
    mostrar_texto(screen, "ENTER: Continuar", WIDTH//2 - 80, HEIGHT-30, small_font)
    
    pygame.display.flip()
    
    # Esperar a que el usuario presione ENTER o cierre la ventana
    esperando = True
    while esperando:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return EXIT
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                esperando = False

    if 'COMPLETA' in resultado:
        return VICTORY
    else:
        return TERMINAL_COMMAND

# ======================
# Pantalla de victoria
# ======================
def mostrar_victoria(screen, font, small_font):
    clock = pygame.time.Clock()
    lineas = [
        "CONEXIÓN SEGURA ESTABLECIDA",
        "SISTEMA LIMPIADO DE INTRUSOS",
        "ACCESOS NO AUTORIZADOS ELIMINADOS",
        "CONFIGURANDO NUEVOS PROTOCOLOS DE SEGURIDAD...",
        "ACTUALIZANDO FIREWALLS...",
        "RECUPERANDO BACKUPS...",
        "SISTEMA ASEGURADO."
    ]
    
    # Animación tipo terminal
    screen.fill(NEGRO)
    tiempo_actual = pygame.time.get_ticks() / 1000
    
    # Primero mostrar la animación de inicialización
    y_pos = 60
    for linea in lineas:
        efecto_maquina_escribir(screen, linea, 50, y_pos, small_font, VERDE_TERMINAL, 15)
        y_pos += 40
        pygame.time.delay(200)
    
    pygame.time.delay(500)
    
    # Después mostrar el mensaje final
    while True:
        tiempo_actual = pygame.time.get_ticks() / 1000
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return EXIT
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN or e.key == pygame.K_ESCAPE:
                    return START_MENU
        
        screen.fill(NEGRO)
        dibujar_efecto_matrix(screen, tiempo_actual)
        pygame.draw.rect(screen, VERDE_TERMINAL, (10, 10, WIDTH-20, HEIGHT-20), 2)
        pygame.draw.rect(screen, VERDE_OSCURO, (10, 10, WIDTH-20, 30))
        mostrar_texto(screen, "SISTEMA DE SEGURIDAD - MISIÓN COMPLETADA", WIDTH//2 - 250, 18, small_font)
        
        # Mensaje de victoria
        mostrar_texto(screen, "MISIÓN EXITOSA", WIDTH//2 - 150, 80, font, VERDE_TERMINAL)
        
        # Mostrar todas las líneas de inicialización de una vez
        y_pos = 150
        for linea in lineas:
            mostrar_texto(screen, linea, 50, y_pos, small_font, VERDE_CLARO)
            y_pos += 30
        
        # Mensaje final
        pygame.draw.rect(screen, NEGRO, (50, 380, WIDTH-100, 80))
        mostrar_texto_con_saltos(screen, HISTORIA["victoria"], 50, 380, small_font, color=AMARILLO_TERMINAL)
        
        # Botón para volver al menú
        accion = dibujar_boton_terminal(screen, "VOLVER AL INICIO", WIDTH//2 - 150, HEIGHT - 100, 300, 50, 
                                        VERDE_TERMINAL, VERDE_CLARO, small_font, START_MENU)
        if accion:
            return accion
        
        # Pie de página
        pygame.draw.rect(screen, VERDE_OSCURO, (10, HEIGHT-40, WIDTH-20, 30))
        mostrar_texto(screen, "ENTER: Volver al inicio", WIDTH//2 - 120, HEIGHT-30, small_font)
        
        pygame.display.flip()
        clock.tick(FPS)

# ======================
# Función principal
# ======================
def main():
    pygame.init()
    pygame.display.set_caption('Cibermisión: Terminal Hacker')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.SysFont('Courier New', 36)
    small_font = pygame.font.SysFont('Courier New', 26)
    
    estado = START_MENU
    parametro = None
    
    # Bucle principal de estados
    while estado != EXIT:
        if estado == START_MENU:
            estado = mostrar_inicio(screen, font, small_font)
        elif estado == TERMINAL_LOGIN:
            estado = terminal_login(screen, font, small_font)
        elif estado == TERMINAL_COMMAND:
            estado, parametro = terminal_comandos(screen, font, small_font, BRUTE_FORCE if parametro is None else parametro)
        elif estado == EMAIL_VIEWER:
            email_index = 0 if parametro is None else parametro
            estado = email_viewer(screen, font, small_font, email_index)
        elif estado == BRUTE_FORCE:
            estado, parametro = jugar_bruteforce(screen, font, small_font)
        elif estado == BINARY_CRACK:
            estado, parametro = jugar_binary_crack(screen, font, small_font)
        elif estado == CIPHER_SPRINT:
            estado = jugar_cipher_sprint(screen, font, small_font)
        elif estado == VICTORY:
            estado = mostrar_victoria(screen, font, small_font)
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()