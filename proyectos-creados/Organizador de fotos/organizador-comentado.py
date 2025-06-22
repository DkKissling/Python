# Importamos las librerías necesarias
import face_recognition as fr  # Librería para detección y reconocimiento facial
import os  # Para trabajar con archivos y directorios
import shutil  # Para copiar archivos entre carpetas

# -------------------------------
# CONFIGURACIÓN DE RUTAS
# -------------------------------

# Carpeta que contiene las fotos desordenadas (todas mezcladas)
fotos_folder = 'Imagenes'

# Carpeta de destino donde organizaremos las fotos por persona
destino_folder = 'Personas_Organizadas'

# Si la carpeta de destino no existe, la creamos
if not os.path.exists(destino_folder):
    os.mkdir(destino_folder)

# -------------------------------
# VARIABLES PARA ORGANIZACIÓN
# -------------------------------

caras_conocidas = []  # Lista donde guardaremos las codificaciones de caras conocidas
nombres_carpetas = []  # Lista de nombres de carpetas asociadas a cada cara

contador_personas = 1  # Contador para asignar nombres únicos: Persona1, Persona2, etc.

# -------------------------------
# PROCESAMIENTO DE CADA FOTO
# -------------------------------

# Recorremos todos los archivos dentro de la carpeta de fotos
for foto in os.listdir(fotos_folder):
    # Construimos la ruta completa a la foto
    path_foto = os.path.join(fotos_folder, foto)

    # Cargamos la imagen usando face_recognition
    imagen = fr.load_image_file(path_foto)

    # Obtenemos todas las codificaciones faciales encontradas en la imagen
    caras = fr.face_encodings(imagen)

    # Si no se encontró ninguna cara, pasamos a la siguiente imagen
    if not caras:
        print(f"Ojo: No hay caras en {foto}")
        continue

    # Tomamos la primera cara detectada en la imagen (suponiendo que hay solo una persona)
    cara_actual = caras[0]

    # Comparamos esta cara con las caras que ya hemos detectado antes
    resultados = fr.compare_faces(caras_conocidas, cara_actual)

    # -------------------------------
    # DETERMINAR SI ES UNA CARA CONOCIDA O NUEVA
    # -------------------------------

    if True in resultados:
        # Si encontramos una coincidencia, obtenemos el índice de esa cara
        indice = resultados.index(True)

        # Con ese índice obtenemos el nombre de la carpeta correspondiente
        nombre_carpeta = nombres_carpetas[indice]
    else:
        # Si la cara no coincide con ninguna conocida, es una persona nueva
        nombre_carpeta = f"Persona{contador_personas}"  # Creamos un nuevo nombre único

        # Guardamos esta cara como nueva cara conocida
        caras_conocidas.append(cara_actual)

        # Guardamos el nombre de su carpeta asociada
        nombres_carpetas.append(nombre_carpeta)

        # Incrementamos el contador para la próxima persona nueva
        contador_personas += 1

        # Creamos la carpeta en destino para esta persona nueva
        os.mkdir(os.path.join(destino_folder, nombre_carpeta))

    # -------------------------------
    # COPIAR LA FOTO A SU CARPETA CORRESPONDIENTE
    # -------------------------------

    # Copiamos la foto original a la carpeta de la persona correspondiente
    shutil.copy(path_foto, os.path.join(destino_folder, nombre_carpeta))

    # Imprimimos confirmación
    print(f"Foto '{foto}' guardada en '{nombre_carpeta}'")

# -------------------------------
# FINAL
# -------------------------------
print("¡Todas las fotos están organizadas!")
