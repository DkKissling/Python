import cv2
import face_recognition as fr

# Cargar imágenes (ya están en formato RGB)
foto_control = fr.load_image_file('FotoA.jpg')
foto_prueba = fr.load_image_file('FotoB.jpg')

# Para mostrar con cv2, necesitamos convertir de RGB a BGR
#Ahora es necesario cambiar la forma que procesan el color 
foto_control_display = cv2.cvtColor(foto_control, cv2.COLOR_RGB2BGR)
foto_prueba_display = cv2.cvtColor(foto_prueba, cv2.COLOR_RGB2BGR)

#mostrar imagenes para saber si esta todo bien 
cv2.imshow('Foto Control', foto_control_display)
cv2.imshow('Foto Prueba', foto_prueba_display)

#para evitar que nuestro programa se cierre una vez abierta las 
#fotos usamos cv2.waitKey(0) si se preciona una tecla
cv2.waitKey(0)
cv2.destroyAllWindows() 