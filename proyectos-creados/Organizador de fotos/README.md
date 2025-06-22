# 📸 Organizador de Fotos por Reconocimiento Facial

## ¿Qué hace este proyecto?
Este script organiza automáticamente tus fotos creando carpetas individuales para cada persona reconocida en tus imágenes utilizando reconocimiento facial.

## Características Principales
- **Reconocimiento Facial Automático**: Identifica rostros sin intervención manual
- **Organización Inteligente**: Crea carpetas individuales para cada persona
- **Procesamiento por Lotes**: Maneja grandes colecciones de fotos
- **Sistema Numerado**: Asigna nombres como Persona1, Persona2 automáticamente

## Requisitos Previos
```bash
pip install face-recognition
pip install opencv-python
```

## Estructura de Carpetas
```
📁 Proyecto/
├── 📄 organizador.py
├── 📁 Imagenes/          # Fotos desordenadas
└── 📁 Personas_Organizadas/  # Resultados organizados
```

## Cómo Usarlo
1. Coloca tus fotos en la carpeta `Imagenes/`
2. Ejecuta el script:
```bash
python organizador.py
```

3. Encuentra tus fotos organizadas en `Personas_Organizadas/`

## Proceso Detallado
1. Escanea todas las imágenes en `Imagenes/`
2. Detecta rostros usando reconocimiento facial
3. Crea carpetas individuales para cada persona detectada
4. Copia cada foto a la carpeta correspondiente

## Ejemplo de Salida
```
Foto 'fiesta.jpg' guardada en 'Persona1'
Foto 'cumple.jpg' guardada en 'Persona2'
Ojo: No hay caras en paisaje.jpg
Foto 'reunion.jpg' guardada en 'Persona1'
¡Todas las fotos están organizadas!
```

## Personalización
Modifica estas variables en el código según tus necesidades:
```python
fotos_folder = 'Imagenes'          # Carpeta de origen
destino_folder = 'Personas_Organizadas'  # Carpeta de destino
```

## Limitaciones
- Funciona mejor con fotos frontales y buena iluminación
- Puede tener dificultades con fotos de baja calidad
- Solo reconoce una cara por foto (la primera que detecta)

## Posibles Mejoras
1. Asignar nombres reales en lugar de Persona1, Persona2
2. Manejar múltiples rostros por foto
3. Añadir interfaz gráfica
4. Opción para mover en lugar de copiar archivos

## Dependencias Clave
- `face_recognition`: Reconocimiento facial
- `os`: Manejo de archivos
- `shutil`: Operaciones de copiado