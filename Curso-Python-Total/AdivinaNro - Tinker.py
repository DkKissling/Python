# Importamos los módulos necesarios
import random  # Para generar números aleatorios
import tkinter as tk  # Para la interfaz gráfica
from tkinter import messagebox  # Para mostrar mensajes emergentes

# Creamos la ventana principal del juego
root = tk.Tk()
root.title("Adivina el Número")  # Título de la ventana
root.geometry("300x250")  # Tamaño inicial de la ventana (ancho x alto)

# Variables globales para el juego
numero_secreto = 0  # Aquí se almacenará el número a adivinar
intentos = 8  # Número máximo de intentos permitidos
nombre_jugador = ""  # Almacenará el nombre del jugador

# Creamos dos frames (marcos) para organizar la interfaz
frame_inicio = tk.Frame(root)  # Frame para la pantalla de inicio
frame_juego = tk.Frame(root)  # Frame para la pantalla de juego

# Elementos de la pantalla de inicio
# Etiqueta con el título del juego
tk.Label(frame_inicio, text="Adivina el Número", font=("Arial", 14)).pack(pady=10)
# Etiqueta para el campo de nombre
tk.Label(frame_inicio, text="Nombre:").pack()

# Campo de entrada para el nombre del jugador
entrada_nombre = tk.Entry(frame_inicio)
entrada_nombre.pack(pady=10)  # Empaquetamos con un poco de espacio vertical

# Elementos de la pantalla de juego
# Etiqueta de bienvenida que mostrará el nombre del jugador
label_bienvenida = tk.Label(frame_juego, font=("Arial", 12))
label_bienvenida.pack(pady=10)

# Etiqueta que muestra los intentos restantes
label_intentos = tk.Label(frame_juego)
label_intentos.pack()

# Etiqueta y campo de entrada para el número
tk.Label(frame_juego, text="Número:").pack()
entrada_numero = tk.Entry(frame_juego)
entrada_numero.pack(pady=5)

# Etiqueta para mostrar si el número es mayor o menor
label_resultado = tk.Label(frame_juego, fg="red")  # Texto en color rojo
label_resultado.pack()

# Función que inicia el juego
def iniciar_juego():
    global nombre_jugador, numero_secreto, intentos  # Accedemos a las variables globales
    
    # Obtenemos el nombre del jugador
    nombre_jugador = entrada_nombre.get()
    if not nombre_jugador:  # Validamos que no esté vacío
        messagebox.showwarning("Error", "Escribe tu nombre")
        return
    
    # Cambiamos de pantalla (ocultamos inicio, mostramos juego)
    frame_inicio.pack_forget()
    frame_juego.pack()
    
    # Generamos un número aleatorio entre 1 y 100
    numero_secreto = random.randint(1, 100)
    intentos = 8  # Reiniciamos los intentos
    
    # Actualizamos las etiquetas
    label_bienvenida.config(text=f"Hola {nombre_jugador}, adivina el número")
    label_intentos.config(text=f"Intentos: {intentos}")
    label_resultado.config(text="")
    entrada_numero.delete(0, tk.END)  # Limpiamos el campo de entrada

# Función que procesa el intento del jugador
def adivinar():
    global intentos  # Accedemos a la variable global
    
    try:
        # Obtenemos el número ingresado por el jugador
        numero = int(entrada_numero.get())
        
        # Validamos que esté entre 1 y 100
        if numero < 1 or numero > 100:
            messagebox.showwarning("Error", "Número entre 1 y 100")
            return
        
        # Restamos un intento
        intentos -= 1
        label_intentos.config(text=f"Intentos: {intentos}")
        
        # Comparamos con el número secreto
        if numero < numero_secreto:
            label_resultado.config(text="¡Más alto!")
        elif numero > numero_secreto:
            label_resultado.config(text="¡Más bajo!")
        else:
            # Si acertó
            messagebox.showinfo("¡Ganaste!", f"¡Correcto! El número era {numero_secreto}")
            reiniciar()  # Volvemos al inicio
            return
        
        # Si se acabaron los intentos
        if intentos == 0:
            messagebox.showinfo("Perdiste", f"Se acabaron los intentos. El número era {numero_secreto}")
            reiniciar()
        
        # Limpiamos el campo de entrada para el próximo intento
        entrada_numero.delete(0, tk.END)
    
    except ValueError:  # Si no ingresó un número válido
        messagebox.showwarning("Error", "Escribe un número")

# Función para volver a la pantalla de inicio
def reiniciar():
    frame_juego.pack_forget()  # Ocultamos el frame de juego
    frame_inicio.pack()  # Mostramos el frame de inicio
    entrada_nombre.delete(0, tk.END)  # Limpiamos el campo de nombre
    entrada_numero.delete(0, tk.END)  # Limpiamos el campo de número

# Botones para las acciones principales
tk.Button(frame_inicio, text="Jugar", command=iniciar_juego).pack()  # Botón de inicio
tk.Button(frame_juego, text="Adivinar", command=adivinar).pack()  # Botón para adivinar

# Mostramos inicialmente la pantalla de inicio
frame_inicio.pack()

# Iniciamos el bucle principal de la aplicación
root.mainloop()