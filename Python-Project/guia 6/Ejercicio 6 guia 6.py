#Hacer una clase Persona con dos métodos: uno para saber si es mayor de edad y 
#el otro para determinar si es varón o mujer. En el programa principal instanciarlo, 
#tomar nombre, edad y sexo, y finalmente mostrar un cartel que diga por ejemplo 
#‘Juan es mayor de edad y es varón’.

class Persona():
   def individuo (self, nombre, edad, sexo):
      self.nombre = nombre
      self.edad = edad
      self.sexo = sexo
      if self.edad>17:
         self.m="mayor"
         return self.m
      elif edad<=17:
         self.m="menor"
         return self.m
   def sexo1 (self):
      if self.sexo == "M" :
         self.genero="varon"
         return self.genero
      if self.sexo == "F":
         self.genero="Mujer"
         return self.genero 
   def mostrarmsj(self):
      msj=(self.nombre + " " + "es" + " " + self.m + " " + "y" + " " + self.genero)
      print (msj)      

r=Persona()
r.individuo("ramon", 27, "M")
r.sexo1()
r.mostrarmsj()
