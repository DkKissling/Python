#Definir una clase Auto con un método que le permita poner la marca y el año.
#En el programa principal declarar tres instancias (objetos), cargarlas y 
#mostrar las marcas de los tres autos.
class autos():
    def __init__(self, marca, año):
        self.marca1=marca
        self.año1=año
auto1=autos("vw",2009)
auto2=autos("fiat",2010)

print (auto1.marca1)
print (auto1.año1)
print (auto2.marca1,auto2.año1)

