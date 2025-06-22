# Importamos las librerías necesarias
import cv2  # Para capturar imágenes desde la cámara y procesar imágenes
import face_recognition as fr  # Para reconocimiento facial
import os  # Para interactuar con el sistema de archivos
import numpy  # Para cálculos numéricos, especialmente arrays
from datetime import datetime  # Para registrar la hora del ingreso

# Definimos la ruta de la carpeta donde están las imágenes de los empleados
ruta = 'Empleados'

# Listas donde se almacenarán las imágenes y los nombres de los empleados
mis_imagenes = []
nombre_empleados = []

# Listamos todos los archivos dentro de la carpeta 'Empleados'
lista_empleados = os.listdir(ruta)

# Recorremos la lista de archivos de empleados
for nombre in lista_empleados:
    imagen_actual = cv2.imread(f'{ruta}\\{nombre}')  # Leemos la imagen
    mis_imagenes.append(imagen_actual)  # Guardamos la imagen en la lista
    nombre_empleados.append(os.path.splitext(nombre)[0])  # Extraemos y guardamos solo el nombre (sin extensión)

# ----------------------------
# FUNCION PARA CODIFICAR ROSTROS
# ----------------------------
def codificar(imagenes):
    lista_codificada = []  # Lista donde se guardarán los rostros codificados

    for imagen in imagenes:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)  # Convertimos la imagen a formato RGB
        codificado = fr.face_encodings(imagen)[0]  # Obtenemos el codificado facial (vector de características)
        lista_codificada.append(codificado)  # Lo añadimos a la lista

    return lista_codificada  # Retornamos la lista de rostros codificados

# ----------------------------
# FUNCION PARA REGISTRAR ASISTENCIA
# ----------------------------
def registrar_ingresos(persona):
    f = open('registro.csv', 'r+')  # Abrimos el archivo para leer y escribir
    lista_datos = f.readlines()  # Leemos todas las líneas del archivo

    nombres_registro = []  # Lista para guardar los nombres ya registrados

    for linea in lista_datos:
        ingreso = linea.strip().split(',')  # Dividimos por coma y eliminamos espacios
        nombres_registro.append(ingreso[0])  # Guardamos solo el nombre

    # Si la persona aún no ha sido registrada, la agregamos al archivo
    if persona not in nombres_registro:
        ahora = datetime.now()  # Obtenemos fecha y hora actual
        string_ahora = ahora.strftime('%H:%M:%S')  # La convertimos a string en formato hora:minuto:segundo
        f.writelines(f'\n{persona},{string_ahora}')  # Escribimos una nueva línea con el nombre y hora

# ----------------------------
# CODIFICAMOS LOS ROSTROS DE LOS EMPLEADOS
# ----------------------------
lista_empleados_codificados = codificar(mis_imagenes)  # Obtenemos los vectores faciales de cada empleado

# ----------------------------
# CAPTURAMOS UNA IMAGEN DESDE LA CAMARA WEB
# ----------------------------
captura = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Iniciamos la cámara (0 es el dispositivo por defecto)
exito, imagen = captura.read()  # Capturamos un fotograma

# Verificamos si la captura fue exitosa
if not exito:
    print("No se ha podido tomar la foto")
else:
    # Detectamos rostros en la imagen capturada
    cara_captura = fr.face_locations(imagen)

    # Codificamos los rostros detectados
    cara_captura_codificada = fr.face_encodings(imagen, cara_captura)

    # Recorremos cada rostro codificado junto con su ubicación
    for caracodif, caraubic in zip(cara_captura_codificada, cara_captura):
        coincidencias = fr.compare_faces(lista_empleados_codificados, caracodif)  # Comparamos con los rostros conocidos
        distancia = fr.face_distance(lista_empleados_codificados, caracodif)  # Calculamos la distancia (mientras menor, más parecido)

        indice_coincidencia = numpy.argmin(distancia)  # Obtenemos el índice de la menor distancia (mejor coincidencia)

        # Si la distancia es mayor a 0.6, consideramos que no hay coincidencia válida
        if distancia[indice_coincidencia] > 0.6:
            print("No coincide con ninguno de nuestros empleados")

        else:
            nombre = nombre_empleados[indice_coincidencia]  # Obtenemos el nombre del empleado correspondiente

            y1, x2, y2, x1 = caraubic  # Coordenadas del rostro detectado

            registrar_ingresos(nombre)  # Registramos su ingreso en el archivo CSV

            # Dibujamos un rectángulo verde alrededor del rostro
            cv2.rectangle(imagen, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Escribimos el nombre del empleado debajo del rostro
            cv2.putText(imagen, nombre, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            # Mostramos la imagen con la cara detectada y nombre
            cv2.imshow('Imagen web', imagen)

            # Esperamos a que se presione una tecla para cerrar la ventana
            cv2.waitKey(0)
