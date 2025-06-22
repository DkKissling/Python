import pygame
import os
import time

def cargar_imagenes(nombre):
    ruta=os.path.join('assets', 'img', nombre)
    try:
        return pygame.image.load(ruta)
    except:
        print("ruta no encontrada")
        return None
    
def cargar_audio(nombre):
    ruta = os.path.join('assets', 'music', nombre)
    try:
        return pygame.mixer.Sound(ruta)
    except:
        print(f"Audio no encontrado en la ruta: {ruta}")
        return None
    
def cargar_efecto(nombre):
    ruta = os.path.join('assets', 'sfx', nombre)
    try:
        return pygame.mixer.Sound(ruta)
    except:
        print(f"Audio no encontrado en la ruta: {ruta}")
        return None

def cargar_documento(tipo, nombre):
    ruta = os.path.join('docs', 'lore', tipo, nombre)
    try:
        with open(ruta, 'r', encoding='utf-8') as archivo:
            return archivo.read()
    except:
        print(f"Documento no encontrado en la ruta: {ruta}")
        return None

#Funcion para manejar el inicio y efecto
def efecto_inicio(pantalla, imagen, posicion, tiempoVisibleInicial, tiempoTitileo, reset=False):    
    if reset or not hasattr(efecto_inicio, 'tiempoInicio'):
        efecto_inicio.tiempoInicio = time.time()
    
    ahora = time.time()
    pasado = ahora - efecto_inicio.tiempoInicio
    if pasado >= tiempoVisibleInicial + tiempoTitileo:
        return False
    
    if pasado < tiempoVisibleInicial:
        pantalla.blit(imagen, posicion)
        return True
    ciclo = int((pasado - tiempoVisibleInicial) / 0.2)  
    
    if ciclo % 2 == 0:
        pantalla.blit(imagen, posicion)
    
    return True


# Función para dibujar el menú (recibe parámetros desde main.py)
def dibujar_menu(pantalla, opciones, indice_seleccionado, fuente_titulo, fuente_opcion, color_base, color_seleccion):
    pantalla.fill((0, 0, 0))  # Fondo negro
    titulo = fuente_titulo.render('HACKER RETRO v1.0', True, color_base)
    pantalla.blit(titulo, (100, 120))
    
    for i, opcion in enumerate(opciones):
        color = color_seleccion if i == indice_seleccionado else color_base
        texto = fuente_opcion.render(opcion, True, color)
        pantalla.blit(texto, (100, 300 + i * 100))

# Función para manejar eventos del menú (retorna el nuevo índice seleccionado)
def manejar_eventos_menu(event, opciones, indice_actual):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_DOWN:
            return (indice_actual + 1) % len(opciones)
        elif event.key == pygame.K_UP:
            return (indice_actual - 1) % len(opciones)
    return indice_actual

#Cargar emails
def cargar_emails(nombre):
    ruta = os.path.join('docs', 'lore', 'emails',nombre)
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()


def abrir_emails(frase_inicial, comando, pantalla, fuente, color, event, input_usuario):
    pantalla.fill((0, 0, 0))  # Fondo negro

    texto_renderizado = fuente.render(frase_inicial + input_usuario, True, color)
    pantalla.blit(texto_renderizado, (50, 50))

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            input_usuario = input_usuario[:-1]
        elif event.key == pygame.K_RETURN:
            if input_usuario.strip().lower() == comando:
                return True, ""  
            else:
                return False, ""  
        else:
            input_usuario += event.unicode

    return False, input_usuario 


def mostrar_emails_en_pantalla(pantalla, fuente, color, contenido_emails):
    pantalla.fill((0, 0, 0))
    y = 50
    for linea in contenido_emails.split('\n'):
        render = fuente.render(linea, True, color)
        pantalla.blit(render, (50, y))
        y += 30


