#Agregar al ejercicio 2 (clase Auto) un método que obtenga la antigüedad. En el programa principal 
#mostrar cuales autos tienen más de 5 años
class Autos ():   
    def __init__(self, marca, año):
        self.marca1=marca
        self.año1=año
    def antiguedad1(self):
        anio=2020
        self.antiguedad= anio-self.año1
x= "si"
masde5anios=[]
while x=="si":
    marca=input("ingrese marca del automovil: ")
    año=int(input("ingrese año de fabricacion: "))
    A=Autos(marca,año)
    A.antiguedad1()
    if A.antiguedad >= 5:
        masde5anios.append(marca)
    x = input("Hay mas? ")
print (masde5anios)