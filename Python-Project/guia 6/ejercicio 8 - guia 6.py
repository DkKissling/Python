#Heredar de la clase Auto una clase Marca, que agregue el atributo Modelo.
#Instanciar en  el programa principal (una sola línea en total). 
#La salida debe ser por ejemplo: Auto: VW Modelo: Gol
class Autos ():   
    def marca(self, marca):
        self.marca1=marca
class Marca(Autos):
    def modelo (self,modelo):
        self.modelo1=modelo
        self.msj=(" Auto: "+ self.marca1 +" Modelo: " + self.modelo1 )

r=Marca()
r.marca("VW")
r.modelo ("Gol")
print (r.msj)