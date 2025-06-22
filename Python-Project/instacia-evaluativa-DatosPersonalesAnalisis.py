Construye un sistema de análisis de datos demográficos que, dadas las listas de nombres, géneros y fechas de nacimiento de una población, pueda calcular y mostrar información relevante, como las iniciales y apellidos de las personas, el nombre más largo, y el promedio de edad de las mujeres en la población. Utiliza estructuras de datos y bucles para procesar la información y generar los resultados requeridos.


# Lista de nombres de personas
nombre = ["Torres, Ana", "Hudson, Kate", "Quesada, Benicio", "Campoamores, Susana", "Santamaria, Carlos", "Skarsgard, Azul", "Catalejos, Walter"]
# Lista de géneros de las personas
sexo = ["f", "f", "m", "f", "m", "f", "m"]
# Lista de fechas de nacimiento de las personas
fecha = ["02/05/1943", "07/09/1984", "10/02/1971", "21/12/1967", "30/01/1982", "30/08/1995", "18/07/1959"]

# Lista para almacenar las iniciales y el apellido de las personas
lista = []
# Extraer iniciales y apellido de las personas y agregarlos a la lista
for i in range(len(nombre)):
    posi = nombre[i].find(",")
    x = nombre[i][posi + 2]
    w = nombre[i][:posi]
    y = x[0]
    lista.append(y + "." + w)

# Imprimir iniciales y apellido de las personas
print("Iniciales y apellido de las personas:")
for i in range(len(nombre)):
    print(lista[i])

# Lista para almacenar los nombres completos de las personas
lista2 = []
# Extraer solo el nombre completo de las personas y agregarlos a la lista
for i in range(len(nombre)):
    posi = nombre[i].find(",")
    x = nombre[i][posi + 2:]
    lista2.append(x)

print(" ")

# Variable para almacenar el nombre más largo
numeromayor = 0
mayor = ""
# Encontrar el nombre más largo en la lista
for i in range(len(lista2)):
    x = len(lista2[i])
    if x > numeromayor:
        numeromayor = x
        mayor = lista2[i]

# Imprimir el nombre más largo
print("El nombre más largo es:", mayor)

# Lista para almacenar las fechas de nacimiento de las mujeres
edades = []
# Filtrar las fechas de nacimiento de las mujeres y agregarlas a la lista de edades
for j in range(len(sexo)):
    if sexo[j] == "f":
        edades.append(fecha[j])

# Listas para almacenar el año, mes y día de las fechas de nacimiento
año = []
año2 = []
dias = []
dias2 = []
meses = []
meses2 = []

# Extraer año, mes y día de las fechas de nacimiento
for i in range(len(edades)):
    posi = edades[i].find("19")
    x = edades[i][posi:]
    año.append(x)
    y = int(año[i])
    año2.append(y)
for i in range(len(edades)):
    posi2 = edades[i].find("/")
    w = edades[i][:posi2]
    dias.append(w)
    q = edades[i][posi + 2]
    meses.append(q)
    a = int(dias[i])
    dias2.append(a)
    b = int(meses[i])
    meses2.append(b)

# Fecha actual
diaHoy = 27
mesHoy = 4
anioHoy = 2020

# Calcular promedio de edad de las mujeres
acumulador = 0
for a in range(len(dias2)):
    edad = anioHoy - año2[a]
    if (meses2[a] > mesHoy) or (meses2[a] == mesHoy and dias2[a] > diaHoy):
        edad -= 1
    acumulador = acumulador + edad

# Imprimir el promedio de edad de las mujeres
print("El promedio de edad de las mujeres es:", acumulador / (len(año2)))
# Lista de nombres de personas
nombre = ["Torres, Ana", "Hudson, Kate", "Quesada, Benicio", "Campoamores, Susana", "Santamaria, Carlos", "Skarsgard, Azul", "Catalejos, Walter"]
# Lista de géneros de las personas
sexo = ["f", "f", "m", "f", "m", "f", "m"]
# Lista de fechas de nacimiento de las personas
fecha = ["02/05/1943", "07/09/1984", "10/02/1971", "21/12/1967", "30/01/1982", "30/08/1995", "18/07/1959"]

# Lista para almacenar las iniciales y el apellido de las personas
lista = []
# Extraer iniciales y apellido de las personas y agregarlos a la lista
for i in range(len(nombre)):
    posi = nombre[i].find(",")
    x = nombre[i][posi + 2]
    w = nombre[i][:posi]
    y = x[0]
    lista.append(y + "." + w)

# Imprimir iniciales y apellido de las personas
print("Iniciales y apellido de las personas:")
for i in range(len(nombre)):
    print(lista[i])

# Lista para almacenar los nombres completos de las personas
lista2 = []
# Extraer solo el nombre completo de las personas y agregarlos a la lista
for i in range(len(nombre)):
    posi = nombre[i].find(",")
    x = nombre[i][posi + 2:]
    lista2.append(x)

print(" ")

# Variable para almacenar el nombre más largo
numeromayor = 0
mayor = ""
# Encontrar el nombre más largo en la lista
for i in range(len(lista2)):
    x = len(lista2[i])
    if x > numeromayor:
        numeromayor = x
        mayor = lista2[i]

# Imprimir el nombre más largo
print("El nombre más largo es:", mayor)

# Lista para almacenar las fechas de nacimiento de las mujeres
edades = []
# Filtrar las fechas de nacimiento de las mujeres y agregarlas a la lista de edades
for j in range(len(sexo)):
    if sexo[j] == "f":
        edades.append(fecha[j])

# Listas para almacenar el año, mes y día de las fechas de nacimiento
año = []
año2 = []
dias = []
dias2 = []
meses = []
meses2 = []

# Extraer año, mes y día de las fechas de nacimiento
for i in range(len(edades)):
    posi = edades[i].find("19")
    x = edades[i][posi:]
    año.append(x)
    y = int(año[i])
    año2.append(y)
for i in range(len(edades)):
    posi2 = edades[i].find("/")
    w = edades[i][:posi2]
    dias.append(w)
    q = edades[i][posi + 2]
    meses.append(q)
    a = int(dias[i])
    dias2.append(a)
    b = int(meses[i])
    meses2.append(b)

# Fecha actual
diaHoy = 27
mesHoy = 4
anioHoy = 2020

# Calcular promedio de edad de las mujeres
acumulador = 0
for a in range(len(dias2)):
    edad = anioHoy - año2[a]
    if (meses2[a] > mesHoy) or (meses2[a] == mesHoy and dias2[a] > diaHoy):
        edad -= 1
    acumulador = acumulador + edad

# Imprimir el promedio de edad de las mujeres
print("El promedio de edad de las mujeres es:", acumulador / (len(año2)))

