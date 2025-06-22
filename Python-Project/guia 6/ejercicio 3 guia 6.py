#3) Usando las clases Operacion y Suma, definir otra que se llame Promedio y utilizarla.
class Operacion():
    def tomoDatos(self):
        self.a = int(input("ingrese primer operando: "))
        self.b = int(input("ingrese segundo operando: "))

    def muestroResultado(self):
        print(self.resu) 

class Suma(Operacion):
    def suma(self):
        self.resu = self.a + self.b

class Promedio(Suma):
    def promedioo(self):
        self.resu=self.resu/2
r = Promedio()
r.tomoDatos()
r.suma()
r.promedioo()
r.muestroResultado()
