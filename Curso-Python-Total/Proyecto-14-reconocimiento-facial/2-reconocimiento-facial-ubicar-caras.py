import cv2
import face_recognition as fr

foto_control = fr.load_image_file('FotoA.jpg')
foto_prueba = fr.load_image_file('FotoB.jpg')

foto_control= cv2.cvtColor(foto_control, cv2.COLOR_RGB2BGR)
foto_prueba = cv2.cvtColor(foto_prueba, cv2.COLOR_RGB2BGR)

#Localizar cara en las imagenes y aunque solo se envie una foto hay que 
# aclara que se esta enviando el primer elemento de esa foto
lugar_cara_A = fr.face_locations(foto_control)[0]
#con esta codificacion solo trasnformamos la imagen en numeros
cara_codificada_A= fr.face_encodings(foto_control)[0]

#ahora vamos a crear un rectangulo para que el humano vea donde esta la cara
#para ello vamos a necesitar la ubicacion obtenida en lugar_cara_A
print(lugar_cara_A) #(139, 454, 268, 325)(top, right, bottom, left)

#parametros que necesitamos son foto, ubicacion de donde hasta donde queremos ir con el rectangulo
#y el color del mismo
cv2.rectangle(foto_control,(lugar_cara_A[3],lugar_cara_A[0]),
              (lugar_cara_A[1],lugar_cara_A[2]),
              (0,255,0))

lugar_cara_B = fr.face_locations(foto_prueba)[0]
cara_codificada_B= fr.face_encodings(foto_prueba)[0]


cv2.rectangle(foto_prueba,(lugar_cara_B[3],lugar_cara_B[0]),
              (lugar_cara_B[1],lugar_cara_B[2]),
              (0,255,0))

cv2.imshow('Foto Control', foto_control)
cv2.imshow('Foto Prueba', foto_prueba)

cv2.waitKey(0)
cv2.destroyAllWindows() 