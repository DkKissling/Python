Dada una cadena de texto que contiene información sobre varias personas en el formato 'nombre-sexo-altura-color_ojos-color_cabello', separa por '/'. Realiza las siguientes tareas:
Obtén la altura promedio de las personas cuya altura está entre 1.70 y 1.80 metros, e imprime sus nombres.
Cuenta la cantidad de mujeres que tienen pelo de color verde-rubio e imprime ese número.

La salida debe mostrar:
La altura promedio del grupo de personas con altura entre 1.70 y 1.80 metros, seguida de sus nombres.
La cantidad de mujeres con pelo verde-rubio.

Ejemplo de entrada:
juan-m-1.78-marron-castaño/pedro-m-1.68-marron-castaño/julia-f-1.71-verde-rubio/ana-f-1.65-verde-rubio/josé-m-1.90-verde-rubio/camila-f-1.73-verde-rubio/laura-f-1.63-verde-rubio/sara-f-1.69-celeste-rubia
Salida esperada:
La altura promedio del primer grupo es: 1.75 y sus nombres son josé,camila
La cantidad de personas del segundo grupo es: 3"

# Definimos una cadena con los datos de las personas
personas = "juan-m-1.78-marron-castaño/pedro-m-1.68-marron-castaño/julia-f-1.71-verde-rubio/ana-f-1.65-verde-rubio/josé-m-1.90-verde-rubio/camila-f-1.73-verde-rubio/laura-f-1.63-verde-rubio/sara-f-1.69-celeste-rubia"
lista = []
individuos = personas.split("/")  # Separamos la cadena en una lista por el carácter '/'

# Creamos listas vacías para almacenar los datos de cada persona
nombre = []
sexo = []
pelo = []
altura = []
medida = []
nombrefinal = []

# Variables para llevar la cuenta
contador = 0
contador2 = 0
acumu = 0

# Iteramos sobre cada individuo en la lista
for i in range(len(individuos)):
    posi = individuos[i].find("-")  # Encontramos la posición del primer guión
    posi2 = individuos[i].find("1")  # Encontramos la posición del primer dígito de la altura
    name = individuos[i][:posi]  # Extraemos el nombre
    nombre.append(name)
    sex = individuos[i][posi + 1]  # Extraemos el sexo
    sexo.append(sex)
    color_de_pelo = individuos[i][posi + 8:]  # Extraemos el color de pelo
    pelo.append(color_de_pelo)
    high = individuos[i][posi2:posi2 + 4]  # Extraemos la altura
    altura.append(high)

# Convertimos las alturas a números flotantes y las almacenamos en la lista 'medida'
for i in range(len(altura)):
    x = float(altura[i])
    medida.append(x)
    # Encontramos las personas con altura entre 1.70 y 1.80
    if medida[i] >= 1.70 and medida[i] <= 1.80:
        y = nombre[i]
        acumu = acumu + medida[i]  # Acumulamos las alturas
        contador2 = contador2 + 1  # Contamos el número de personas
        promedio = acumu / (contador2)  # Calculamos el promedio
        nombrefinal.append(y)  # Agregamos el nombre a la lista 'nombrefinal'
    # Contamos el número de mujeres con pelo verde-rubio
    if sexo[i] == "f" and pelo[i] == "verde-rubio":
        contador = contador + 1

print(" ")
print("La altura promedio del primer grupo es:", promedio, "y sus nombres son", nombrefinal)
print(" ")
print("La cantidad de personas del segundo grupo es: ", contador)

# Unimos los nombres en 'nombrefinal' en una cadena separada por comas
nombrefinalstring = ",".join(nombrefinal)
print(" ")
print("La altura promedio del primer grupo es:", promedio, "y sus nombres son", nombrefinalstring)
print(" ")
