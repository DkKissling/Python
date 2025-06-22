#Hacer una clase Teléfono con los atributos marca, modelo y costo mensual y 
# un método que muestre (o devuelva) el costo anual.
class telefono():
    def __init__(self,marca,modelo,Cm):
        self.marca1=marca
        self.modelo1=modelo
        self.Cm1=Cm
    def anual (self):
        Ca= self.Cm1*12
        return Ca
a= telefono("alcatel", "500", 500)

print (a.anual())