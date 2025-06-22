Agrega una nueva función al programa de análisis de datos de Spotify para calcular el promedio de visualizaciones por álbum para todas las bandas. Esta función debe recorrer todas las bandas, calcular el total de visualizaciones y dividirlo por el número total de álbumes de todas las bandas. Luego, muestra este promedio al usuario.

# Datos de las bandas y solistas
genero = ["B", "B", "B", "S", "S"]  # B para bandas, S para solistas
bandas = ["Led Zeppelin", "Rage Against the Machine", "Seru Giran", "Peter Gabriel", "Jeff Beck"]
albunes = [9, 4, 5, 10, 3]  # Cantidad de álbumes
miembros = ["Jimmy Page", "Robert Plant (voz)", "John Bonham", "John Paul Jones",
            "Zack de la Rocha (voz)", "Tom Morello", "Tim Commerford", "Brad Wilk",
            "Pedro Aznar", "Oscar Moro", "David Lebón (voz)", "Charly García (voz)"]
vp = [1234567, 2434908, 324192, 70, 76]  # Visualizaciones en Spotify

# Definición de la clase base Composicion
class Composicion:
    def datos(self, nombre, albunes):
        self.nombre = nombre
        self.albun = albunes

# Definición de la clase Bandas que hereda de Composicion
class Bandas(Composicion):
    def __init__(self, visualizacion):
        self.visualizacion = visualizacion

# Definición de la clase Solistas que hereda de Composicion
class Solistas(Composicion):
    def __init__(self, edad):
        self.edad = edad

# Definición de la clase Spotify para realizar análisis de datos
class Spotify:
    # Método para calcular el total de visualizaciones de todas las bandas
    def contador(self):
        conta = 0
        for i in range(len(vp)):
            if genero[i] == "B":
                x = Bandas(vp[i])
                conta = x.visualizacion + conta
        return conta

    # Método para obtener los apellidos de los solistas
    def apellidodesolistas(self):
        for i in range(len(genero)):
            ApeSolista = []
            if genero[i] == "S":
                y = Solistas(vp[i])
                y.datos(bandas[i], albunes[i])
                w = y.nombre.find(" ")
                if w > 1:
                    ApeSolista.append(y.nombre[w + 1:])
                print(ApeSolista)

    # Método para obtener los nombres de los vocalistas de las bandas
    def vocalistas(self):
        for i in range(len(vp)):
            nomvocal = []
            if genero[i] == "B":
                z = Bandas(vp[i])
                for e in range(len(miembros)):
                    z.datos(miembros[e], albunes[i])
                    vocal = z.nombre.find("(voz)")
                    if vocal > 0:
                        nomvocal.append(z.nombre[:vocal])
                return nomvocal

    # Método para encontrar al solista con más álbumes
    def mayor1(self):
        mayo = 0
        for i in range(len(albunes)):
            masmejor = []
            x = Solistas(vp[i])
            x.datos(bandas[i], albunes[i])
            if x.albun > mayo:
                mayo = x.albun
                if mayo == 10:
                    masmejor.append(x.nombre)
                    return masmejor

# Instanciar la clase Spotify y llamar a sus métodos
r = Spotify()
print(r.contador())
print(r.apellidodesolistas())
print(r.vocalistas())
print(r.mayor1())
# Datos de las bandas y solistas
genero = ["B", "B", "B", "S", "S"]  # B para bandas, S para solistas
bandas = ["Led Zeppelin", "Rage Against the Machine", "Seru Giran", "Peter Gabriel", "Jeff Beck"]
albunes = [9, 4, 5, 10, 3]  # Cantidad de álbumes
miembros = ["Jimmy Page", "Robert Plant (voz)", "John Bonham", "John Paul Jones",
            "Zack de la Rocha (voz)", "Tom Morello", "Tim Commerford", "Brad Wilk",
            "Pedro Aznar", "Oscar Moro", "David Lebón (voz)", "Charly García (voz)"]
vp = [1234567, 2434908, 324192, 70, 76]  # Visualizaciones en Spotify

# Definición de la clase base Composicion
class Composicion:
    def datos(self, nombre, albunes):
        self.nombre = nombre
        self.albun = albunes

# Definición de la clase Bandas que hereda de Composicion
class Bandas(Composicion):
    def __init__(self, visualizacion):
        self.visualizacion = visualizacion

# Definición de la clase Solistas que hereda de Composicion
class Solistas(Composicion):
    def __init__(self, edad):
        self.edad = edad

# Definición de la clase Spotify para realizar análisis de datos
class Spotify:
    # Método para calcular el total de visualizaciones de todas las bandas
    def contador(self):
        conta = 0
        for i in range(len(vp)):
            if genero[i] == "B":
                x = Bandas(vp[i])
                conta = x.visualizacion + conta
        return conta

    # Método para obtener los apellidos de los solistas
    def apellidodesolistas(self):
        for i in range(len(genero)):
            ApeSolista = []
            if genero[i] == "S":
                y = Solistas(vp[i])
                y.datos(bandas[i], albunes[i])
                w = y.nombre.find(" ")
                if w > 1:
                    ApeSolista.append(y.nombre[w + 1:])
                print(ApeSolista)

    # Método para obtener los nombres de los vocalistas de las bandas
    def vocalistas(self):
        for i in range(len(vp)):
            nomvocal = []
            if genero[i] == "B":
                z = Bandas(vp[i])
                for e in range(len(miembros)):
                    z.datos(miembros[e], albunes[i])
                    vocal = z.nombre.find("(voz)")
                    if vocal > 0:
                        nomvocal.append(z.nombre[:vocal])
                return nomvocal

    # Método para encontrar al solista con más álbumes
    def mayor1(self):
        mayo = 0
        for i in range(len(albunes)):
            masmejor = []
            x = Solistas(vp[i])
            x.datos(bandas[i], albunes[i])
            if x.albun > mayo:
                mayo = x.albun
                if mayo == 10:
                    masmejor.append(x.nombre)
                    return masmejor

# Instanciar la clase Spotify y llamar a sus métodos
r = Spotify()
print(r.contador())
print(r.apellidodesolistas())
print(r.vocalistas())
print(r.mayor1())

