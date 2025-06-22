#Definir una clase que al ser instanciada reciba un valor numérico y cargue una lista de nombres 
#hasta esa cantidad. Hacer también un método que muestre la lista completa.

class Persona:
    def __init__ (self, numero):
        self.lista=[]
        for i in range (numero):
            self.nombre=input("ingresar un nombre: ")
            self.lista.append(self.nombre) 
    def mostrarlista(self):
        print (self.lista)  

r=Persona(3)
r.mostrarlista()
