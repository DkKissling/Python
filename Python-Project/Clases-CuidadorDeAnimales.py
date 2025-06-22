Desarrolla un programa que simule la gestión de una jaula que alberga pumas y venados. La jaula puede contener diferentes cantidades de cada uno de estos animales. Los pumas y venados tienen características específicas, como el peso y la edad, que afectan su estado de salud. Utiliza clases para representar a los animales y a la jaula, y permite al usuario ingresar información sobre los animales en la jaula. El programa debería poder mostrar el estado de salud de los animales en la jaula.

class Animal():
    def salud(self,peso,pesosano):
        if peso>=pesosano:
            return ("sano")
        elif peso<pesosano:
            return("enfermo")


class Puma(Animal):
    pesoideal=200
    
    def __init__(self,numero,edad,peso):
        self.numero = numero
        self.edad = edad
        self.peso = peso


    def vejez (self):
        self.contador=0
        if self.edad>5:
            self.contador=self.contador+1



class Venado(Animal):
    pesoideal=140
    def __init__(self,numero,peso):
        self.numero1 = numero
        self.peso1 = peso


class Jaula():
    def __init__ (self,cantidad,clase):
        self.lista=[]       
        if clase=="Puma":
            for i in range (cantidad):
                self.pregunta2=int (input("peso del puma: "))
                self.pregunta3=int (input("edad: "))
                x=Puma(i+1,self.pregunta2,self.pregunta3)
                self.lista.append (x)
        elif clase== "Venado":
            for i in range (cantidad):
                self.pregunta2=int (input("peso del Venado: "))
                x=Venado(i+1,self.pregunta2)
                self.lista.append (x)

    def GetSeter(self):
        print ("jaula de pumas")
        for i in self.lista:
            print (i.numero,i.salud)

jaula1=Jaula(2,"Puma")
jaula1.GetSeter
            
"""
Jaula de Pumas
# 1 - sano
# 2 - enfermo
# 3 - sano
Cantidad de adultos: 2

Jaula de Venados
# 1 enfermo
# 2 sano

"""

