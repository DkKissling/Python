import cv2
import face_recognition as fr
import os
import numpy
from datetime import datetime


ruta='Empleados'
mis_imagenes=[]
nombre_empleados=[]
lista_empleados=os.listdir(ruta)

for nombre in lista_empleados:
    imagen_actual=cv2.imread(f'{ruta}\{nombre}')
    mis_imagenes.append(imagen_actual)
    nombre_empleados.append(os.path.splitext(nombre)[0])

#codificar imagenes

def codificar (imagenes):

    #Creamos una lista codificada 
    lista_codificada = []

    #pasar las imagenes a rgb
    for imagen in imagenes:
        imagen= cv2.cvtColor(imagen,cv2.COLOR_BGR2RGB)

        #Ccodificamos las imagenes 
        codificado = fr.face_encodings(imagen)[0]

        #agregar a la nueva lista
        lista_codificada.append(codificado)
    
    #devolver lista codificada
    return lista_codificada

#Registrar asistencia
def registrar_ingresos(persona):
    f=open('registro.csv','r+')
    lista_datos=f.readline()
    nombres_registro=[]
    for linea in lista_datos:
        ingreso = linea.split(',')
        nombres_registro.append(ingreso[0])
    
    if persona not in nombres_registro:
        ahora =datetime.now()
        string_ahora=ahora.strftime('%H:%M%S')
        f.writelines(f'\n{persona},{string_ahora}')


lista_empleados_codificados=codificar(mis_imagenes)

#Tomar una imagen de camara web
captura= cv2.VideoCapture(0,cv2.CAP_DSHOW)

#leer la imagen de la camara tomo 
exito, imagen = captura.read()

if not exito:
    print("no se ha podido tomar la foto ")
else:
    #reconocer si hay una cara o no 
    cara_captura=fr.face_locations(imagen)

    #codificar la cara capturada
    cara_captura_codificada=fr.face_encodings(imagen,cara_captura)

    #buscar coincidencias 
    for caracodif, caraubic in zip(cara_captura_codificada,cara_captura):
        coincidencias=fr.compare_faces(lista_empleados_codificados,caracodif)
        distancia=fr.face_distance(lista_empleados_codificados,caracodif)

        indice_coincidencia = numpy.argmin(distancia)

        #mostrar coincidencias 
        if distancia[indice_coincidencia]>0.6:
            print("No coincide con ninguno de nuestros empleados ")

        else:
            #Buscar el nombnre del empleado 
            nombre=nombre_empleados[indice_coincidencia]

            #de aca sacamos los 4 valores que necesitamos
            y1,x2,y2,x1=caraubic

            registrar_ingresos(nombre)


            #Creamos un rectangulo para que se vea el nombre y lugar donde esta la cara
            cv2.rectangle(imagen,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.putText(imagen,nombre,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            #mostrar imagen obtenido por la camara
            cv2.imshow('Imagen web', imagen)

            #mantener la ventana abierta 
            cv2.waitKey(0)



