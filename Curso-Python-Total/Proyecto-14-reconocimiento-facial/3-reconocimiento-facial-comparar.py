import cv2
import face_recognition as fr

foto_control = fr.load_image_file('FotoA.jpg')
foto_prueba = fr.load_image_file('FotoB.jpg')

foto_control = cv2.cvtColor(foto_control, cv2.COLOR_RGB2BGR)
foto_prueba = cv2.cvtColor(foto_prueba, cv2.COLOR_RGB2BGR)

lugar_cara_A = fr.face_locations(foto_control)[0]
cara_codificada_A = fr.face_encodings(foto_control)[0]


cv2.rectangle(foto_control, (lugar_cara_A[3], lugar_cara_A[0]),
              (lugar_cara_A[1], lugar_cara_A[2]),
              (0, 255, 0))

lugar_cara_B = fr.face_locations(foto_prueba)[0]
cara_codificada_B = fr.face_encodings(foto_prueba)[0]

cv2.rectangle(foto_prueba, (lugar_cara_B[3], lugar_cara_B[0]),
              (lugar_cara_B[1], lugar_cara_B[2]),
              (0, 255, 0))

#Realizar comparacion de caras usamos compare_faces
#esta funcion requiere una lista como parametro y un objeto con el cual comparar  
resultado= fr.compare_faces([cara_codificada_A],cara_codificada_B)
#con esto vemos si es verdadeo o falso segun los parametros de 0.6 que es el valor que sea por defecto 
print(resultado)


#podemos ajustar los parametros pero tenemos que ver cual es la distancia entre fotos primero 
distancia = fr.face_distance([cara_codificada_A],cara_codificada_B)
print(distancia)


#para cambiar la tolerancia a la comparacion agregamos un valor mas a resultado 
resultado2= fr.compare_faces([cara_codificada_A],cara_codificada_B,0.3)
print(resultado2)

cv2.imshow('Foto Control', foto_control)
cv2.imshow('Foto Prueba', foto_prueba)

cv2.waitKey(0)
cv2.destroyAllWindows()
