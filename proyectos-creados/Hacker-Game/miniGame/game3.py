import pygame
import sys
import json
import random
import time
import os

# ======================
# Configuración general
# ======================
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
GRIS = (100, 100, 100)
MORADO = (128, 0, 128)

# Estados de juego
START_MENU, STORY_INTRO, BRUTE_FORCE, BINARY_CRACK, CIPHER_SPRINT, VICTORY, EXIT = range(7)

# ======================
# Narrativa del juego
# ======================
HISTORIA = {
    "intro": "Año 2055. Eres un agente de ciberseguridad. Has detectado una intrusión en el sistema central. Debes navegar por el sistema para detener al hacker antes de que robe información confidencial.",
    "brute_force": "NIVEL 1: El primer nivel de seguridad está bloqueado. Necesitas adivinar la contraseña usando fuerza bruta para avanzar.",
    "binary_crack": "NIVEL 2: Has entrado al segundo nivel, pero necesitas descifrar los códigos binarios para continuar.",
    "cipher_sprint": "NIVEL 3: ¡Última barrera! Intercepta y escribe rápidamente las palabras clave para bloquear al intruso.",
    "victoria": "¡Misión completada! Has detenido al hacker y salvado los datos confidenciales. El sistema está seguro gracias a ti, agente."
}

# ======================
# Funciones de utilidades
# ======================

def mostrar_texto(screen, texto, x, y, font, color=BLANCO):
    img = font.render(texto, True, color)
    screen.blit(img, (x, y))

def mostrar_texto_con_saltos(screen, texto, x, y, font, max_width=700, line_height=35, color=BLANCO):
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

def dibujar_boton(screen, texto, x, y, w, h, color_inactivo, color_activo, font, accion=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(screen, color_activo, (x, y, w, h))
        if click[0] == 1 and accion is not None:
            return accion
    else:
        pygame.draw.rect(screen, color_inactivo, (x, y, w, h))
        
    text_surf = font.render(texto, True, NEGRO)
    text_rect = text_surf.get_rect(center=((x + w/2), (y + h/2)))
    screen.blit(text_surf, text_rect)
    return None

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

# ======================
# Pantallas de historia
# ======================
def mostrar_pantalla_historia(screen, font, historia_key, siguiente_estado):
    clock = pygame.time.Clock()
    texto = HISTORIA[historia_key]
    
    while True:
        screen.fill((20, 20, 40))  # Fondo azul oscuro
        
        # Dibujar borde decorativo
        pygame.draw.rect(screen, MORADO, (30, 30, WIDTH-60, HEIGHT-60), 3)
        
        # Título
        mostrar_texto(screen, "MISIÓN: CIBERDEFENSA", WIDTH//2 - 200, 60, font, VERDE)
        
        # Historia
        mostrar_texto_con_saltos(screen, texto, 50, 150, pygame.font.SysFont(None, 34), max_width=700)
        
        # Botón para continuar
        accion = dibujar_boton(screen, "Continuar →", WIDTH//2 - 100, HEIGHT - 100, 200, 50, VERDE, (100, 255, 100), font)
        if accion:
            return siguiente_estado
            
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return EXIT
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return siguiente_estado
                
        pygame.display.flip()
        clock.tick(FPS)

# ======================
# Mini-juego: BruteForce
# ======================
def jugar_bruteforce(screen, font, archivo_json, max_errores=5):
    data = cargar_json_seguro(archivo_json)
    palabra, pista = random.choice(list(data.items()))
    letras_correctas = ['_' for _ in palabra]
    intento = ''
    errores = 0
    terminado = False
    clock = pygame.time.Clock()

    while True:
        screen.fill((20, 20, 40))  # Color consistente con la historia
        pygame.draw.rect(screen, MORADO, (20, 20, WIDTH-40, HEIGHT-40), 3)  # Borde decorativo
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return EXIT
            if not terminado and e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    if intento == palabra:
                        letras_correctas = list(palabra)
                        terminado = True
                    else:
                        for i, c in enumerate(intento[:len(palabra)]):
                            if c == palabra[i]: letras_correctas[i] = c
                        errores += 1
                        if errores >= max_errores:
                            terminado = True
                        intento = ''
                elif e.key == pygame.K_BACKSPACE:
                    intento = intento[:-1]
                else:
                    if e.unicode.isalpha(): intento += e.unicode.lower()

        mostrar_texto(screen, '🔒 NIVEL 1: Adivina la Contraseña', WIDTH//2-250, 40, font, VERDE)
        mostrar_texto(screen, f'Pista: {pista}', 50, 100, font)
        mostrar_texto(screen, ' '.join(letras_correctas), 50, 170, font, VERDE)
        mostrar_texto(screen, f'Intento: {intento}', 50, 240, font)
        mostrar_texto(screen, f'Errores: {errores}/{max_errores}', 50, 310, font, ROJO)

        if terminado:
            msg = '✅ ¡Nivel superado!' if errores < max_errores and ''.join(letras_correctas) == palabra else f"❌ Nivel fallido. La contraseña era '{palabra}'"
            clr = VERDE if '✅' in msg else ROJO
            mostrar_texto(screen, msg, 50, 380, font, clr)
            pygame.display.flip()
            pygame.time.wait(2000)
            if '✅' in msg:
                return BINARY_CRACK
            else:
                return BRUTE_FORCE  # Reintentar el nivel

        pygame.display.flip()
        clock.tick(FPS)

# ======================
# Mini-juego: CodeBuster (Binary Crack)
# ======================
def jugar_binary_crack(screen, font, small_font):
    codes = [("01001000", "H"), ("01100001", "a"), ("01100011", "c"), ("01101011", "k"), ("01100101", "e"), ("01110010", "r")]
    binary_dict = {chr(i): format(i, '08b') for i in range(65, 91)}  # A-Z
    binary_dict.update({chr(i): format(i, '08b') for i in range(97, 123)})  # a-z
    current = 0
    input_text = ''
    attempts = 3
    show_help = False
    clock = pygame.time.Clock()

    while True:
        screen.fill((20, 20, 40))  # Color consistente
        pygame.draw.rect(screen, MORADO, (20, 20, WIDTH-40, HEIGHT-40), 3)  # Borde decorativo
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return EXIT
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_TAB:
                    show_help = not show_help
                elif e.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif e.key == pygame.K_RETURN:
                    if input_text.strip().upper() == codes[current][1].upper():
                        current += 1
                        input_text = ''
                        attempts = 3
                        if current >= len(codes):
                            # Mostrar la palabra completa antes de continuar
                            screen.fill((20, 20, 40))
                            pygame.draw.rect(screen, MORADO, (20, 20, WIDTH-40, HEIGHT-40), 3)
                            mostrar_texto(screen, '🔓 NIVEL 2: Descifre Binario - COMPLETADO', 50, 50, font, VERDE)
                            palabra_completa = ''.join([code[1] for code in codes])
                            mostrar_texto(screen, f'¡Has descifrado la palabra "{palabra_completa}"!', 50, 150, font, VERDE)
                            mostrar_texto(screen, 'Continuando a la siguiente fase...', 50, 250, font)
                            pygame.display.flip()
                            pygame.time.wait(2000)
                            return CIPHER_SPRINT
                    else:
                        attempts -= 1
                        input_text = ''
                        if attempts <= 0:
                            return BINARY_CRACK  # Reintentar nivel
                else:
                    input_text += e.unicode

        mostrar_texto(screen, '🔓 NIVEL 2: Descifre Binario', 50, 50, font, VERDE)
        mostrar_texto(screen, f'Código {current+1}/{len(codes)}: {codes[current][0]}', 50, 120, font, VERDE)
        mostrar_texto(screen, f'Tu respuesta: {input_text}', 50, 200, font)
        mostrar_texto(screen, f'Intentos restantes: {attempts}', 50, 260, small_font, ROJO)
        mostrar_texto(screen, 'Presiona TAB para ayuda', 50, 300, small_font)

        # Progreso
        mostrar_texto(screen, 'Progreso:', 50, 350, small_font)
        palabra_actual = ''.join([codes[i][1] if i < current else "_" for i in range(len(codes))])
        mostrar_texto(screen, palabra_actual, 150, 350, small_font, VERDE)

        if show_help:
            # Mostrar tabla de ayuda en formato de cuadrícula
            y0 = 390
            filas = 4
            cols = 7
            w_celda = 100
            h_celda = 35
            mostrar_texto(screen, 'Tabla ASCII-Binario:', 50, y0-30, small_font, (255,255,0))
            
            items = list(binary_dict.items())[:26]  # Solo las letras que necesitamos
            for i, (k, v) in enumerate(items):
                fila = i // cols
                col = i % cols
                x = 50 + col * w_celda
                y = y0 + fila * h_celda
                pygame.draw.rect(screen, (50, 50, 70), (x, y, w_celda-5, h_celda-5), 1)
                mostrar_texto(screen, f'{k}: {v}', x+5, y+5, small_font, (200, 200, 255))

        pygame.display.flip()
        clock.tick(FPS)

# ======================
# Mini-juego: CipherSprint
# ======================
def jugar_cipher_sprint(screen, font, ruta_json, small_font=None):
    # Si no se proporciona small_font, crear uno
    if small_font is None:
        small_font = pygame.font.SysFont(None, 28)
    
    try:    
        data = cargar_json_seguro(ruta_json)
        frases = data.get('mensajes_confidenciales', [])
        # Si no hay datos en el JSON o está vacío, usar frases de respaldo
        if not frases:
            frases = [
                "El acceso a la información confidencial ha sido bloqueado exitosamente.",
                "Los protocolos de seguridad han sido restablecidos en todos los servidores.",
                "El intruso ha sido detectado y eliminado del sistema central.",
                "Todos los archivos sensibles están ahora protegidos con cifrado de nivel militar.",
                "El cortafuegos ha sido actualizado para prevenir futuros intentos de intrusión."
            ]
        frase = random.choice(frases)
    except FileNotFoundError:
        # Si no se encuentra el archivo, usar frases predefinidas
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
    clock = pygame.time.Clock()

    resultado = None
    # Bucle de tipeo
    while resultado is None:
        elapsed = time.time() - start
        remaining = max(0, tiempo_lim - elapsed)
        
        # Verificar condiciones de fin de juego
        if remaining <= 0:
            resultado = '¡Se acabó el tiempo!'
        elif intentos <= 0:
            resultado = '¡Te quedaste sin intentos!'
        elif idx >= len(a_tipear):
            resultado = '¡MISIÓN CUMPLIDA!'
        
        # Si ya tenemos un resultado, salimos del bucle
        if resultado is not None:
            break

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return EXIT
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_BACKSPACE:
                    text_in = text_in[:-1]
                elif e.key == pygame.K_RETURN:
                    if text_in.strip().lower() == a_tipear[idx].lower():
                        idx += 1
                    else:
                        intentos -= 1
                    text_in = ''
                else:
                    text_in += e.unicode

        screen.fill((20, 20, 40))
        pygame.draw.rect(screen, MORADO, (20, 20, WIDTH-40, HEIGHT-40), 3)
        
        mostrar_texto(screen, '🔐 NIVEL 3: Sprint de Cifrado', WIDTH//2-170, 40, font, VERDE)
        mostrar_texto(screen, 'Tipea rápidamente las palabras interceptadas:', 50, 100, small_font)
        
        # Mostrar progreso de palabras
        progreso = f"Palabras: {idx}/{len(a_tipear)}"
        mostrar_texto(screen, progreso, 50, 150, font, VERDE)
        
        # Sólo mostramos la palabra actual si todavía quedan palabras por tipear
        if idx < len(a_tipear):
            mostrar_texto(screen, f'Palabra actual: {a_tipear[idx]}', 50, 200, font, AZUL)
        else:
            mostrar_texto(screen, '¡Completado!', 50, 200, font, VERDE)
            
        mostrar_texto(screen, f'Ingresado: {text_in}', 50, 260, font, AZUL)
        mostrar_texto(screen, f'Intentos: {intentos}', 50, 320, font, ROJO)
        
        # Barra de tiempo
        tiempo_porcentaje = remaining / tiempo_lim
        ancho_barra = int(700 * tiempo_porcentaje)
        pygame.draw.rect(screen, GRIS, (50, 380, 700, 30))
        pygame.draw.rect(screen, VERDE if tiempo_porcentaje > 0.3 else ROJO, (50, 380, ancho_barra, 30))
        mostrar_texto(screen, f'{int(remaining)}s', 400, 385, small_font, NEGRO)
        
        pygame.display.flip()
        clock.tick(FPS)

    # Pantalla de resultado
    screen.fill((20, 20, 40))
    pygame.draw.rect(screen, MORADO, (20, 20, WIDTH-40, HEIGHT-40), 3)
    
    color = VERDE if 'CUMPLIDA' in resultado else ROJO
    mostrar_texto(screen, resultado, WIDTH//2 - 150, 100, font, color)
    
    if 'CUMPLIDA' in resultado:
        mostrar_texto(screen, 'Mensaje desbloqueado:', 50, 180, font, VERDE)
        
        # Dividir la frase en múltiples líneas
        mostrar_texto_con_saltos(screen, frase, 50, 240, font, max_width=700, color=BLANCO)
        
        mostrar_texto(screen, "Presiona ENTER para continuar...", WIDTH//2 - 200, 500, font, VERDE)
    else:
        mostrar_texto(screen, 'No lograste desbloquear el mensaje.', 50, 180, font, ROJO)
        mostrar_texto(screen, "Presiona ENTER para reintentar...", WIDTH//2 - 200, 500, font, ROJO)
    
    pygame.display.flip()
    
    # Esperar a que el usuario presione ENTER o cierre la ventana
    esperando = True
    while esperando:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return EXIT
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                esperando = False

    if 'CUMPLIDA' in resultado:
        return VICTORY
    else:
        return CIPHER_SPRINT  # Reintentar nivel

# ======================
# Pantalla de victoria final
# ======================
def mostrar_victoria(screen, font):
    clock = pygame.time.Clock()
    
    while True:
        screen.fill((20, 20, 40))
        pygame.draw.rect(screen, VERDE, (20, 20, WIDTH-40, HEIGHT-40), 5)
        
        mostrar_texto(screen, "¡MISIÓN COMPLETADA!", WIDTH//2 - 180, 100, font, VERDE)
        mostrar_texto_con_saltos(screen, HISTORIA["victoria"], 50, 200, font, max_width=700)
        
        # Botón para volver al menú
        accion = dibujar_boton(screen, "Volver al Inicio", WIDTH//2 - 150, HEIGHT - 100, 300, 60, AZUL, (100, 100, 255), font)
        if accion:
            return START_MENU
            
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return EXIT
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return START_MENU
                
        pygame.display.flip()
        clock.tick(FPS)

# ======================
# Pantalla de inicio
# ======================
def mostrar_inicio(screen, font):
    clock = pygame.time.Clock()
    
    while True:
        screen.fill((20, 20, 40))
        pygame.draw.rect(screen, MORADO, (20, 20, WIDTH-40, HEIGHT-40), 3)
        
        mostrar_texto(screen, "CIBERMISIÓN: PROTEGE EL SISTEMA", WIDTH//2 - 300, 100, font, VERDE)
        mostrar_texto(screen, "Una aventura hacker", WIDTH//2 - 150, 170, pygame.font.SysFont(None, 36), BLANCO)
        
        # Botón de inicio
        accion = dibujar_boton(screen, "INICIAR MISIÓN", WIDTH//2 - 150, HEIGHT//2, 300, 70, VERDE, (100, 255, 100), font)
        if accion:
            return STORY_INTRO
            
        # Botón de salida
        accion = dibujar_boton(screen, "SALIR", WIDTH//2 - 100, HEIGHT//2 + 100, 200, 50, ROJO, (255, 100, 100), font)
        if accion:
            return EXIT
            
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return EXIT
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    return STORY_INTRO
                elif e.key == pygame.K_ESCAPE:
                    return EXIT
                
        pygame.display.flip()
        clock.tick(FPS)

# ======================
# Bucle principal y menú
# ======================
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Cibermisión: Protege el Sistema')
    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 28)

    estado = START_MENU
    
    while estado != EXIT:
        if estado == START_MENU:
            estado = mostrar_inicio(screen, font)
        elif estado == STORY_INTRO:
            estado = mostrar_pantalla_historia(screen, font, "intro", BRUTE_FORCE)
        elif estado == BRUTE_FORCE:
            estado = mostrar_pantalla_historia(screen, font, "brute_force", BRUTE_FORCE)
            if estado == BRUTE_FORCE:
                estado = jugar_bruteforce(screen, font, os.path.join('docs', 'palabras.json'))
        elif estado == BINARY_CRACK:
            estado = mostrar_pantalla_historia(screen, font, "binary_crack", BINARY_CRACK)
            if estado == BINARY_CRACK:
                estado = jugar_binary_crack(screen, font, small_font)
        elif estado == CIPHER_SPRINT:
            estado = mostrar_pantalla_historia(screen, font, "cipher_sprint", CIPHER_SPRINT)
            if estado == CIPHER_SPRINT:
                estado = jugar_cipher_sprint(screen, font, os.path.join('docs', 'confidencial.json'), small_font)
        elif estado == VICTORY:
            estado = mostrar_victoria(screen, font)

    pygame.quit()

if __name__ == '__main__':
    main()