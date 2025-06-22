import random
import tkinter as tk
from tkinter import messagebox

class AhorcadoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego del Ahorcado")
        self.root.geometry("500x600")
        
        # Variables del juego
        self.palabras = ["elefante", "manzana", "bici", "montaña", "guitarra", 
                        "pelota", "compu", "mariposa", "camión", "abogado"]
        self.palabra_secreta = ""
        self.letras_adivinadas = []
        self.vidas = 6
        self.gano = False
        
        # Interfaz gráfica
        self.crear_interfaz()
        self.iniciar_juego()
    
    def crear_interfaz(self):
        # Frame principal
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack(expand=True, fill='both')
        
        # Elementos de la interfaz
        self.label_titulo = tk.Label(self.frame, text="Juego del Ahorcado", font=("Arial", 18, "bold"))
        self.label_titulo.pack(pady=10)
        
        self.label_estado = tk.Label(self.frame, text="", font=("Arial", 12))
        self.label_estado.pack(pady=5)
        
        self.label_palabra = tk.Label(self.frame, text="", font=("Courier", 24))
        self.label_palabra.pack(pady=20)
        
        self.label_ahorcado = tk.Label(self.frame, text="", font=("Courier", 14))
        self.label_ahorcado.pack(pady=10)
        
        self.label_vidas = tk.Label(self.frame, text="", font=("Arial", 12))
        self.label_vidas.pack(pady=5)
        
        self.entry_letra = tk.Entry(self.frame, font=("Arial", 16), width=3)
        self.entry_letra.pack(pady=10)
        
        self.btn_probar = tk.Button(self.frame, text="Probar Letra", command=self.probar_letra)
        self.btn_probar.pack(pady=10)
        
        self.btn_reiniciar = tk.Button(self.frame, text="Nuevo Juego", command=self.iniciar_juego)
        self.btn_reiniciar.pack(pady=10)
    
    def iniciar_juego(self):
        self.palabra_secreta = random.choice(self.palabras)
        self.letras_adivinadas = []
        self.vidas = 6
        self.gano = False
        
        self.actualizar_interfaz()
        self.entry_letra.focus_set()
    
    def actualizar_interfaz(self):
        # Mostrar progreso de la palabra
        progreso = ""
        for letra in self.palabra_secreta:
            if letra in self.letras_adivinadas:
                progreso += letra + " "
            else:
                progreso += "_ "
        self.label_palabra.config(text=progreso)
        
        # Mostrar estado del ahorcado
        ahorcado = ""
        if self.vidas <= 5: ahorcado += "  O  \n"
        if self.vidas <= 4: ahorcado += "  |  \n"
        if self.vidas <= 3: ahorcado += " /|  \n"
        if self.vidas <= 2: ahorcado += " /|\\ \n"
        if self.vidas <= 1: ahorcado += " /   \n"
        if self.vidas <= 0: ahorcado += " / \\ "
        self.label_ahorcado.config(text=ahorcado)
        
        # Mostrar vidas restantes
        self.label_vidas.config(text=f"Vidas restantes: {self.vidas}")
        
        # Verificar si ganó
        if "_" not in progreso:
            self.gano = True
            messagebox.showinfo("¡Ganaste!", f"¡Felicidades! Adivinaste la palabra: {self.palabra_secreta}")
        
        # Verificar si perdió
        if self.vidas <= 0 and not self.gano:
            messagebox.showinfo("Perdiste", f"La palabra era: {self.palabra_secreta}")
    
    def probar_letra(self):
        letra = self.entry_letra.get().lower()
        self.entry_letra.delete(0, tk.END)
        
        if not letra or len(letra) != 1 or not letra.isalpha():
            messagebox.showerror("Error", "Por favor ingresa una sola letra")
            return
        
        if letra in self.letras_adivinadas:
            messagebox.showwarning("Ya probaste", f"Ya probaste con la letra '{letra}'")
            return
        
        self.letras_adivinadas.append(letra)
        
        if letra not in self.palabra_secreta:
            self.vidas -= 1
        
        self.actualizar_interfaz()

# Iniciar la aplicación
root = tk.Tk()
app = AhorcadoApp(root)
root.mainloop()