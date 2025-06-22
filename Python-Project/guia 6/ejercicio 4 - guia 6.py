#Definir una clase Persona cuyo constructor reciba nombre y edad.El programa principal pedirá en 
#forma repetitiva (hasta que no haya más) los mismos datos, hará la instanciación de un objeto y 
#lo agregará en una lista.Por lo tanto, los elementos de dicha lista serán objetos y 
#podrá mostrarse por recorrido y/o por subindicación.
class Persona:
    def __init__(self,nombre,edad):
        self.a = nombre
        self.b= edad        


x= "si"
lista=[]
while x=="si":
    nombre=input("ingrese nombre: ")
    edad=int(input("ingrese la edad"))
    p=Persona(nombre,edad)
    lista.append(p)
    x = input("Hay mas? ")

r=Persona()
r.a()
r.b()





        

