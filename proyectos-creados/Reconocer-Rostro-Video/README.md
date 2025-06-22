# 🎥 Reconocimiento de Rostros en Video

## 🔍 Descripción  
Este proyecto detecta la presencia de una persona específica en un video utilizando reconocimiento facial. Guarda los frames donde aparece la persona y genera un reporte detallado con los momentos exactos de detección.

## 🚀 Características Principales
- **Detección en Tiempo Real**: Analiza videos frame por frame
- **Sistema de Reportes**: Genera CSV con tiempos exactos de detección
- **Almacenamiento Automático**: Guarda frames con detecciones positivas
- **Configuración Flexible**: Ajusta sensibilidad y frecuencia de análisis

## ⚙️ Requisitos
```bash
pip install face-recognition opencv-python numpy
```

## 📁 Estructura de Archivos
```
📂 proyecto/
├── 📄 main.py                 # Script principal
├── 📁 fotos_perfil/           # Fotos de referencia (misma persona)
├── 📹 video.mp4               # Video a analizar
└── 📁 frames_detectados/      # Resultados (se crea automáticamente)
    ├── 📄 detecciones.csv     # Reporte de detecciones
    └── 🖼️ frame_XXX.jpg       # Frames con detecciones
```

## 🛠️ Configuración
Personaliza estos parámetros en el código:
```python
CARPETA_FOTOS = "fotos_perfil"     # Carpeta con fotos de referencia
VIDEO_PATH = "video.mp4"            # Video a analizar
CARPETA_SALIDA = "frames_detectados" # Carpeta para resultados
FRAME_INTERVAL = 5                 # Analizar cada 5 frames (ajustar para rendimiento)
TOLERANCE = 0.5                    # Sensibilidad (0.6=estricto, 0.4=flexible)
```

## ▶️ Cómo Usar
1. Coloca varias fotos de la persona en `fotos_perfil/` (mientras más, mejor)
2. Pon el video a analizar como `video.mp4` en la raíz
3. Ejecuta el script:
```bash
python main.py
```

4. Encuentra los resultados en `frames_detectados/`

## 📊 Reporte CSV
El archivo `detecciones.csv` contiene:
```csv
Frame,Segundo
120,4.32
240,8.15
360,12.02
```

## 💡 Consejos para Mejor Detección
1. Usa fotos de referencia con buena iluminación y rostro frontal
2. Reduce `FRAME_INTERVAL` para análisis más preciso (más lento)
3. Ajusta `TOLERANCE` según necesidad:
   - 0.6 → Menos falsos positivos (puede perder detecciones)
   - 0.4 → Más detecciones (puede incluir falsos positivos)

## 📝 Ejemplo de Salida
```
[INFO] Cargando imágenes de referencia...
[OK] Cargada imagen: persona1.jpg
[WARN] No se detectó rostro en foto_borrosa.jpg
[INFO] Procesando video...
[DETECTADO] Frame 120 (4.32 seg) → guardado.
[DETECTADO] Frame 240 (8.15 seg) → guardado.
[INFO] Proceso terminado.
Frames procesados: 1000
Frames guardados con detección: 2
Reporte CSV generado en: frames_detectados/detecciones.csv
```

## ⚠️ Limitaciones
- Requiere varias fotos de referencia de buena calidad
- El rendimiento depende de la longitud del video
- Puede tener dificultades con ángulos extremos o poca luz
- Solo detecta una cara por frame

## 🔜 Mejoras Futuras
1. Soporte para múltiples personas
2. Interfaz gráfica de usuario
3. Procesamiento en tiempo real con cámara web
4. Exportar clips de video con las detecciones

## 📚 Dependencias Clave
| Biblioteca | Función |
|------------|---------|
| `face_recognition` | Reconocimiento facial |
| `opencv-python` | Procesamiento de video |
| `csv` | Generación de reportes |
| `os` | Manejo de archivos |
