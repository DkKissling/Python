Implementa una función en la clase Nombres2008 que permita calcular la diferencia entre el número de personas con un nombre específico de un género dado en dos años diferentes (2008 y 2018). La función debe tomar como entrada el nombre y el género, y devolver la diferencia en el número de personas con ese nombre entre los dos años.


class Nombres2008:
    nombres = "Eva,17039,f,Daniel,19005,m,Emily,17434,f,Emma,18813,f,Ethan,20216,m,Julia,18616,f,Jacob,22594,m,Joshua,19205,m,Michael,20626,m,Olivia,17081,f"
    nombres_m = ["Emma", "Olivia", "Ava", "Isabella", "Sophia"]
    nombres_h = ["Liam", "Noah", "Michael", "James", "Oliver"]
    numeros_h = [19837, 18267, 14516, 13525, 13389]
    numeros_m = [18688, 17921, 14924, 14464, 13928]

    @staticmethod
    def extraer_datos():
        nombres = []
        numeros = []
        sexo = []
        mujeres = []
        hombres = []

        individuos = Nombres2008.nombres.split(",")
        for i in range(len(individuos)):
            if individuos[i].isalpha() and len(individuos[i]) > 2:
                nombres.append(individuos[i])
            elif individuos[i].isalpha() and len(individuos[i]) < 2:
                sexo.append(individuos[i])
            elif individuos[i].isdigit():
                numeros.append(individuos[i])

        for j in range(len(nombres)):
            if sexo[j] == "f":
                mujeres.append(nombres[j])
            elif sexo[j] == "m":
                hombres.append(nombres[j])

        return mujeres, hombres, numeros

    @staticmethod
    def buscar_nombre(nombre, anio):
        nombres_m, nombres_h, _ = Nombres2008.extraer_datos()
        nombres_totales = nombres_m + nombres_h
        nombre_minusculas = nombre.lower()
        
        if anio == 2008:
            return nombre_minusculas in " ".join(nombres_totales).lower()
        elif anio == 2018:
            nombres_totales_2018 = Nombres2008.nombres_m + Nombres2008.nombres_h
            return nombre_minusculas in " ".join(nombres_totales_2018).lower()
        else:
            return "El año es incorrecto"

    @staticmethod
    def diferencia(posicion, sexo):
        _, _, numeros = Nombres2008.extraer_datos()
        numeros_h = Nombres2008.numeros_h
        numeros_m = Nombres2008.numeros_m
        
        if sexo == "m":
            return int(numeros_h[posicion - 1]) - int(numeros[posicion - 1])
        elif sexo == "f":
            return int(numeros_m[posicion - 1]) - int(numeros[posicion - 1])

    @staticmethod
    def buscar_caracter(caracter):
        nombres_m, nombres_h, _ = Nombres2008.extraer_datos()
        nombres_totales = nombres_m + nombres_h
        nombres_coincidentes = [nombre for nombre in nombres_totales if caracter.lower() in nombre.lower()]
        return nombres_coincidentes

    @staticmethod
    def nombres_repetidos(*nombres):
        nombres_m, nombres_h, _ = Nombres2008.extraer_datos()
        nombres_totales = nombres_m + nombres_h
        nombres_repetidos = [nombre for nombre in nombres if nombres_totales.count(nombre) > 1]
        return nombres_repetidos


# Ejemplos de uso:
print(Nombres2008.diferencia(1, "m"))
print(Nombres2008.diferencia(2, "f"))
print(Nombres2008.buscar_caracter("J"))
print(Nombres2008.nombres_repetidos("Emma", "Daniel", "Olivia"))
class Nombres2008:
    nombres = "Eva,17039,f,Daniel,19005,m,Emily,17434,f,Emma,18813,f,Ethan,20216,m,Julia,18616,f,Jacob,22594,m,Joshua,19205,m,Michael,20626,m,Olivia,17081,f"
    nombres_m = ["Emma", "Olivia", "Ava", "Isabella", "Sophia"]
    nombres_h = ["Liam", "Noah", "Michael", "James", "Oliver"]
    numeros_h = [19837, 18267, 14516, 13525, 13389]
    numeros_m = [18688, 17921, 14924, 14464, 13928]

    @staticmethod
    def extraer_datos():
        nombres = []
        numeros = []
        sexo = []
        mujeres = []
        hombres = []

        individuos = Nombres2008.nombres.split(",")
        for i in range(len(individuos)):
            if individuos[i].isalpha() and len(individuos[i]) > 2:
                nombres.append(individuos[i])
            elif individuos[i].isalpha() and len(individuos[i]) < 2:
                sexo.append(individuos[i])
            elif individuos[i].isdigit():
                numeros.append(individuos[i])

        for j in range(len(nombres)):
            if sexo[j] == "f":
                mujeres.append(nombres[j])
            elif sexo[j] == "m":
                hombres.append(nombres[j])

        return mujeres, hombres, numeros

    @staticmethod
    def buscar_nombre(nombre, anio):
        nombres_m, nombres_h, _ = Nombres2008.extraer_datos()
        nombres_totales = nombres_m + nombres_h
        nombre_minusculas = nombre.lower()
        
        if anio == 2008:
            return nombre_minusculas in " ".join(nombres_totales).lower()
        elif anio == 2018:
            nombres_totales_2018 = Nombres2008.nombres_m + Nombres2008.nombres_h
            return nombre_minusculas in " ".join(nombres_totales_2018).lower()
        else:
            return "El año es incorrecto"

    @staticmethod
    def diferencia(posicion, sexo):
        _, _, numeros = Nombres2008.extraer_datos()
        numeros_h = Nombres2008.numeros_h
        numeros_m = Nombres2008.numeros_m
        
        if sexo == "m":
            return int(numeros_h[posicion - 1]) - int(numeros[posicion - 1])
        elif sexo == "f":
            return int(numeros_m[posicion - 1]) - int(numeros[posicion - 1])

    @staticmethod
    def buscar_caracter(caracter):
        nombres_m, nombres_h, _ = Nombres2008.extraer_datos()
        nombres_totales = nombres_m + nombres_h
        nombres_coincidentes = [nombre for nombre in nombres_totales if caracter.lower() in nombre.lower()]
        return nombres_coincidentes

    @staticmethod
    def nombres_repetidos(*nombres):
        nombres_m, nombres_h, _ = Nombres2008.extraer_datos()
        nombres_totales = nombres_m + nombres_h
        nombres_repetidos = [nombre for nombre in nombres if nombres_totales.count(nombre) > 1]
        return nombres_repetidos


# Ejemplos de uso:
print(Nombres2008.diferencia(1, "m"))
print(Nombres2008.diferencia(2, "f"))
print(Nombres2008.buscar_caracter("J"))
print(Nombres2008.nombres_repetidos("Emma", "Daniel", "Olivia"))

