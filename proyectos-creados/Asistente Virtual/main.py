# main.py

import threading
import tkinter as tk
from tkinter import Entry, Text, Scrollbar, END

# Importa la clase AsistenteVirtual del archivo asistenteVirtual.py
from asistenteVirtual import AsistenteVirtual

# -------------------------------------------------
# Creamos la ventana principal de Tkinter
# -------------------------------------------------
ventana = tk.Tk()
ventana.title("Asistente Virtual 2.0")
ventana.geometry("1000x400")
ventana.resizable(False, False)
ventana.config(bg="#10324f")

# -------------------------------------------------
# Creamos el área de consola (Text + Scrollbar)
# -------------------------------------------------
consola_frame = tk.Frame(ventana, bg="#222222")
consola_frame.place(x=610, y=10, width=380, height=380)

consola = Text(
    consola_frame,
    bg="#1e1e1e",
    fg="white",
    font=("Courier", 12),
    wrap="word",
    bd=0
)
consola.place(x=0, y=0, width=360, height=380)

scroll = Scrollbar(consola_frame, command=consola.yview)
scroll.place(x=360, y=0, width=20, height=380)
consola.configure(yscrollcommand=scroll.set)

# -------------------------------------------------
# Instanciamos el asistente virtual
# -------------------------------------------------
asistente = AsistenteVirtual(path_json_comandos="comandos.json")

# Guardamos la referencia al método original para TTS
_hablar_original = asistente.hablar

# -------------------------------------------------
# Sobrescribimos el método hablar(...) del asistente
# Para que, además de hacer TTS, inserte el mensaje en la consola
# -------------------------------------------------
def hablar_y_loguear(mensaje: str):
    """
    Este método hijackea al hablar original:
    1) Inserta en la consola de texto lo que dice el asistente
    2) Llama al método TTS original (_hablar_original)
    """
    consola.insert(END, f"Asistente: {mensaje}\n")
    consola.see(END)
    _hablar_original(mensaje)

# Reemplazamos el método hablar de la instancia por nuestro wrapper
asistente.hablar = hablar_y_loguear

# -------------------------------------------------
# SALUDO AL INICIAR (programado con after para que se ejecute
# una vez que la ventana ya esté abierta)
# -------------------------------------------------
def saludo_inicial_despues_de_cargar():
    # Llamamos al saludo_inicial() para que el asistente hable y lo muestre en consola
    asistente.saludo_inicial()

# Programamos el saludo para que ocurra 200 ms después de que la ventana se dibuje
ventana.after(200, saludo_inicial_despues_de_cargar)

# -------------------------------------------------
# Variables y funciones para el modo “escucha continua”
# -------------------------------------------------
listening_active = False          # Indica si el hilo de escucha está activo
listening_thread = None           # Referencia al hilo que ejecuta la escucha en bucle

def listening_loop():
    """
    Bucle que se ejecuta en un hilo aparte.  
    Mientras listening_active == True, llama a transformar_audio_en_texto(),
    muestra el texto como “Usuario: …” en consola y llama a ejecutar_comando().
    """
    global listening_active

    while listening_active:
        # 1) Mostrar en consola que está escuchando
        consola.insert(END, "Escuchando...\n")
        consola.see(END)

        # 2) Esperar audio hasta que detecte silencio (1.8 s)
        texto_reconocido = asistente.transformar_audio_en_texto()

        if not listening_active:
            # Si alguien pulsó “Detener” mientras esperábamos audio, salimos
            break

        if not texto_reconocido:
            # Si no entendió nada, avisar y seguir el bucle
            asistente.hablar("No entendí, ¿podés repetir?")
            continue

        # 3) Si reconoció algo, lo mostramos como “Usuario: …”
        consola.insert(END, f"Usuario: {texto_reconocido}\n")
        consola.see(END)

        # 4) Ejecutamos el comando reconocido
        try:
            encontrado = asistente.ejecutar_comando(texto_reconocido)
        except SystemExit:
            # Si el usuario dijo “cerrar” o similar, paramos todo
            listening_active = False
            ventana.destroy()
            return

        if not encontrado:
            asistente.hablar("Lo siento, no sé cómo responder a eso.")

    # Cuando listening_active quede en False, el hilo terminará y liberamos referencia
    return

# -------------------------------------------------
# Función que se llama al presionar el botón “🎤 Escuchar” (o “■ Detener”):
#   Alterna entre iniciar el hilo de escucha y detenerlo
# -------------------------------------------------
def toggle_listen():
    global listening_active, listening_thread

    if not listening_active:
        # Si no estaba escuchando, arrancamos la escucha continua
        listening_active = True
        boton_escuchar.config(text="■ Detener", bg="#dc3545")  # Cambiamos texto y color

        # Iniciamos el hilo de escucha si no había uno activo
        if not listening_thread or not listening_thread.is_alive():
            listening_thread = threading.Thread(target=listening_loop, daemon=True)
            listening_thread.start()
    else:
        # Si ya estaba escuchando, detenemos el bucle
        listening_active = False
        boton_escuchar.config(text="🎤 Escuchar", bg="#28a745")

# -------------------------------------------------
# Función que se llama al presionar “Enviar” (texto manual):
#   1. Lee el texto del Entry
#   2. Lo muestra como “Usuario: …” en consola
#   3. Llama a asistente.ejecutar_comando(texto)
# -------------------------------------------------
def enviar_texto():
    texto = entrada.get().strip()
    if not texto:
        return

    # 1) Mostramos en consola lo que escribió el usuario
    consola.insert(END, f"Usuario: {texto}\n")
    consola.see(END)
    entrada.delete(0, END)

    # 2) Llamamos al asistente para ejecutar el comando
    try:
        encontrado = asistente.ejecutar_comando(texto)
        if not encontrado:
            asistente.hablar("Lo siento, no sé cómo responder a eso.")
    except SystemExit:
        # Si el usuario dio un comando de cierre, cerramos la ventana
        ventana.destroy()

# -------------------------------------------------
# Campo de entrada (Entry) y botón “Enviar”
# -------------------------------------------------
entrada = Entry(
    ventana,
    font=("Helvetica", 14),
    bd=0,
    relief=tk.FLAT,
    width=30
)
entrada.place(x=100, y=300, height=40, width=300)

boton_enviar = tk.Button(
    ventana,
    text="Enviar",
    font=("Helvetica", 12),
    bg="#1c8adb",
    fg="white",
    relief=tk.FLAT,
    command=enviar_texto
)
boton_enviar.place(x=410, y=300, height=40, width=80)

# -------------------------------------------------
# Botón “Escuchar” (ahora es un toggle entre “Escuchar” y “Detener”)
# -------------------------------------------------
boton_escuchar = tk.Button(
    ventana,
    text="🎤 Escuchar",
    font=("Helvetica", 16),
    bg="#28a745",    # Verde cuando está en modo “Escuchar”
    fg="white",
    relief=tk.FLAT,
    command=toggle_listen
)
boton_escuchar.place(x=230, y=150, width=150, height=50)

# -------------------------------------------------
# Línea divisoria vertical
# -------------------------------------------------
linea_divisoria = tk.Frame(ventana, bg="white", width=2, height=400)
linea_divisoria.place(x=600, y=0)

# -------------------------------------------------
# -----------------------------------
# Finalmente, arrancamos el loop de Tkinter
# -----------------------------------
ventana.mainloop()
