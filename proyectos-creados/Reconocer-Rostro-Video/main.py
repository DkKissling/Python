import face_recognition
import cv2
import os
import csv

# Configuración
CARPETA_FOTOS = "fotos_perfil"   # varias fotos de la MISMA persona
VIDEO_PATH = "video.mp4"
CARPETA_SALIDA = "frames_detectados"
FRAME_INTERVAL = 5
TOLERANCE = 0.5  # tolerancia del match

# Crear carpeta de salida si no existe
os.makedirs(CARPETA_SALIDA, exist_ok=True)

# Paso 1: Cargar todas las fotos de referencia
print("[INFO] Cargando imágenes de referencia...")
known_face_encodings = []

for filename in os.listdir(CARPETA_FOTOS):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(CARPETA_FOTOS, filename)
        image = face_recognition.load_image_file(image_path)
        
        encodings = face_recognition.face_encodings(image)
        if len(encodings) > 0:
            encoding = encodings[0]
            known_face_encodings.append(encoding)
            print(f"[OK] Cargada imagen: {filename}")
        else:
            print(f"[WARN] No se detectó rostro en {filename}")

if len(known_face_encodings) == 0:
    print("[ERROR] No se pudo cargar ningún rostro de referencia.")
    exit()

# Paso 2: Abrir video
print("[INFO] Procesando video...")
video_capture = cv2.VideoCapture(VIDEO_PATH)

fps = video_capture.get(cv2.CAP_PROP_FPS)
frame_count = 0
saved_frame_count = 0

# CSV para reporte
csv_path = os.path.join(CARPETA_SALIDA, "detecciones.csv")
csv_file = open(csv_path, mode='w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Frame", "Segundo"])

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Procesar solo cada FRAME_INTERVAL frames
    if frame_count % FRAME_INTERVAL == 0:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Comparar contra todos los encodings de referencia
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=TOLERANCE)
            match_found = any(matches)

            if match_found:
                # Dibujar rectángulo y etiqueta
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, "MATCH", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

                # Guardar frame
                frame_filename = f"{CARPETA_SALIDA}/frame_{frame_count}.jpg"
                cv2.imwrite(frame_filename, frame)
                saved_frame_count += 1

                # Guardar en CSV
                segundo = frame_count / fps
                csv_writer.writerow([frame_count, round(segundo, 2)])

                print(f"[DETECTADO] Frame {frame_count} ({round(segundo,2)} seg) → guardado.")
                # Si solo te interesa la PRIMER detección en el frame, podrías poner: break

    frame_count += 1

# Cleanup
video_capture.release()
cv2.destroyAllWindows()
csv_file.close()

print(f"[INFO] Proceso terminado.")
print(f"Frames procesados: {frame_count}")
print(f"Frames guardados con detección: {saved_frame_count}")
print(f"Reporte CSV generado en: {csv_path}")
