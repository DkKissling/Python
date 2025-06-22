import pygame
import sys

pygame.init()

# Configuración inicial
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Binary Crack")

font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 32)
clock = pygame.time.Clock()

# Códigos binarios para adivinar
codes = [("01000001", "A"), ("01000010", "B"), ("01001000 01101001", "Hi")]
current = 0
input_text = ""
attempts_left = 3
show_help = False
message = ""
message_timer = 0  # Para controlar la duración del mensaje
game_over = False  # Estado del juego para saber si ha terminado

# Tabla de conversión básica
binary_dict = {
    "A": "01000001", "B": "01000010", "C": "01000011", "D": "01000100",
    "E": "01000101", "F": "01000110", "G": "01000111", "H": "01001000",
    "I": "01001001"
}

# Función para renderizar texto
def draw_text(text, x, y, size=font, color=(255, 255, 255)):
    surface = size.render(text, True, color)
    screen.blit(surface, (x, y))

def draw_help_table():
    y = 300
    draw_text("Diccionario binario:", 50, y - 3, small_font, (255, 255, 0))
    for letter, binary in binary_dict.items():
        draw_text(f"{letter} : {binary}", 50, y+25, small_font)
        y += 25

# Loop principal
while True:
    screen.fill((0, 0, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif event.key == pygame.K_RETURN and not game_over:
                if input_text.strip().upper() == codes[current][1].upper():
                    message = "¡Correcto!"
                    message_timer = pygame.time.get_ticks()  # Timer para el mensaje
                    current += 1
                    if current >= len(codes):
                        message = "¡Ganaste el juego!"
                        game_over = True  # El juego ha terminado
                        pygame.display.flip()
                        pygame.time.wait(1000)
                    else:
                        input_text = ""  # Solo limpiar la respuesta cuando se adivina correctamente
                        attempts_left = 3  # Resetear intentos para el siguiente código
                else:
                    attempts_left -= 1
                    if attempts_left == 0:
                        message = f"¡Perdiste! Era: {codes[current][1]}"
                        message_timer = pygame.time.get_ticks()  # Timer para el mensaje
                        game_over = True  # El juego ha terminado
                        pygame.display.flip()
                        pygame.time.wait(1000)
                    else:
                        input_text = ""  # Limpiar la respuesta y permitir nuevo intento
            elif event.key == pygame.K_TAB:
                show_help = not show_help
            else:
                input_text += event.unicode

    # Mostrar código binario actual
    if current < len(codes) and not game_over:
        draw_text("Descifra el código binario:", 50, 50)
        draw_text(codes[current][0], 50, 100, font, (0, 255, 0))
        draw_text("Tu respuesta: " + input_text, 50, 180)
        draw_text(f"Intentos restantes: {attempts_left}", 50, 230, small_font, (255, 150, 150))
        draw_text("Presiona TAB para mostrar/ocultar tabla de ayuda", 50, 270, small_font, (200, 200, 200))
        if show_help:
            draw_help_table()

    # Mostrar mensaje de victoria o derrota si el juego terminó
    if game_over:
        draw_text(message, 50, HEIGHT - 500, font, (0, 255, 0) if "Ganaste" in message else (255, 0, 0))

    # Limpiar mensaje después de un tiempo
    if message and pygame.time.get_ticks() - message_timer >= 1500 and not game_over:
        message = ""  # Limpiar mensaje después de un tiempo

    pygame.display.flip()
    clock.tick(60)
