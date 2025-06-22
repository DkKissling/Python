import face_recognition as fr
import os
import shutil

# Carpeta con las fotos desordenadas
fotos_folder = 'Imagenes'
# Carpeta donde guardaremos las fotos ordenadas
destino_folder = 'Personas_Organizadas'

# Crear carpeta de destino si no existe
if not os.path.exists(destino_folder):
    os.mkdir(destino_folder)

# Aquí guardaremos las caras conocidas
caras_conocidas = []
nombres_carpetas = []

# Empezamos en 1 para Persona1, Persona2, etc.
contador_personas = 1

for foto in os.listdir(fotos_folder):
    # Cargamos la foto
    path_foto = os.path.join(fotos_folder, foto)
    imagen = fr.load_image_file(path_foto)
    
    # Buscamos caras en la foto
    caras = fr.face_encodings(imagen)
    
    # Si no hay caras, pasamos a la siguiente foto
    if not caras:
        print(f"Ojo: No hay caras en {foto}")
        continue
    
    # Tomamos la primera cara que encontremos
    cara_actual = caras[0]
    
    # Comparamos con las caras que ya conocemos
    resultados = fr.compare_faces(caras_conocidas, cara_actual)
    
    # Si encontramos una coincidencia
    if True in resultados:
        indice = resultados.index(True)
        nombre_carpeta = nombres_carpetas[indice]
    else:
        # Si es una cara nueva
        nombre_carpeta = f"Persona{contador_personas}"
        caras_conocidas.append(cara_actual)
        nombres_carpetas.append(nombre_carpeta)
        contador_personas += 1
        
        # Creamos carpeta para esta persona
        os.mkdir(os.path.join(destino_folder, nombre_carpeta))
    
    # Copiamos la foto a su carpeta
    shutil.copy(path_foto, os.path.join(destino_folder, nombre_carpeta))
    print(f"Foto '{foto}' guardada en '{nombre_carpeta}'")

print("¡Todas las fotos están organizadas!")