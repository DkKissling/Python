#Definir una clase Telefono, sus atributos son: marca, modelo, sistema operativo (nombre y 
#versión, ejemplo: Android 9), plan(costo) y cantidad de RAM. Sus métodos son: costo anual, 
#mostrar versión (Sistema Operativo xxxxx, versión x.x) y si es gama alta o no (con 6 o más gigas 
#de RAM) .

class Telefono():
    def __init__ (self, marca,modelo,SO,Plan,Ram):
        self.marca = marca
        self.modelo = modelo
        self.sistemaOpertivo= SO  
        self.Plan=Plan
        self.Ram=Ram
    def costoA(self):
        self.costoAnual = self.Plan*12
        msj=str(self.costoAnual)
        msj1="su costo anual es : "+msj
        return msj1
    def version(self):
        sistema=self.sistemaOpertivo.split(" ")
        self.x=("sistema: "+sistema[0]+", "+"Version: "+sistema[1])
        return self.x
    def gama (self):
        q=int(self.Ram)
        if q>=6:
            self.y="gama alta"
        elif q<6:
            self.y="gama baja pobre"
        return self.y
r=Telefono("Motorola","PlayG8","Android 9",1500, 6)
r.costoA()
r.version()   
r.gama()
print (r.costoA())
print (r.version())
print (r.gama())