import tkinter as tk
from tkinter import PhotoImage
from tkinter import Entry
from PIL import Image, ImageTk

def enviar_comando():
    comando = entrada.get().strip()
    if comando:
        print(f"Comando enviado: {comando}")
        entrada.delete(0, tk.END)

def activar_voz():
    print("Activando micrófono...")

# --- Ventana principal ---
ventana = tk.Tk()
ventana.title("Asistente Moderno")
ventana.geometry("600x400")
ventana.resizable(False, False)

# --- Fondo ---
fondo_imagen = Image.open("fondo.jpg")
fondo_imagen = fondo_imagen.resize((600, 400))
fondo = ImageTk.PhotoImage(fondo_imagen)

canvas = tk.Canvas(ventana, width=600, height=800)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=fondo, anchor="nw")

# --- Entrada redondeada ---
entrada_frame = tk.Frame(ventana, bg="#FFFFFF", bd=0)
entrada = Entry(entrada_frame, font=("Helvetica", 14), bd=0, relief=tk.FLAT, width=30)
entrada.pack(padx=10, pady=10)
entrada_frame.place(x=100, y=300, height=50, width=340)

# --- Botón flecha (enviar) ---
flecha_img = Image.open("flecha.png").resize((40, 40))
flecha_icono = ImageTk.PhotoImage(flecha_img)

boton_flecha = tk.Button(ventana, image=flecha_icono, command=enviar_comando,
                         bd=0, bg="#FFFFFF", activebackground="#DDDDDD", relief=tk.FLAT)
boton_flecha.place(x=450, y=300)

# Cargar imagen con transparencia
micro_img = Image.open("microfono1.png").convert("RGBA").resize((80, 80))
micro_icono = ImageTk.PhotoImage(micro_img)
canvas_micro = canvas.create_image(300, 140, image=micro_icono)
def on_click_micro(event):
    activar_voz()

canvas.tag_bind(canvas_micro, "<Button-1>", on_click_micro)


ventana.mainloop()
