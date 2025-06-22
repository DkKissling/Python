# Asistente Virtual 2.0

Un asistente virtual inteligente que puede hablar, escuchar y ejecutar comandos por voz o texto en español argentino.

## Características

### 🎤 Reconocimiento de Voz
- Reconocimiento de voz en español argentino
- Escucha continua con botón de activación/desactivación
- Entrada de texto manual como alternativa

### 🗣️ Síntesis de Voz
- Respuestas por voz en español
- Configuración de voz femenina (Helena)
- Registro de conversaciones en consola

### 🔧 Comandos Disponibles

#### Información Básica
- **Fecha y hora**: "¿qué día es hoy?", "decime la hora"
- **Saludo inteligente**: Saluda según la hora del día

#### Navegación Web
- **YouTube**: "abrir youtube", "reproducir música de rock"
- **Google**: "abrir navegador"
- **Búsquedas**: "busca en internet Python", "busca en wikipedia Argentina"

#### Entretenimiento
- **Chistes**: "contame un chiste", "decime una broma"

#### Información en Tiempo Real
- **Clima**: "¿qué tiempo hace en Buenos Aires?"
- **Noticias**: "últimas noticias"
- **Acciones**: "precio de las acciones de Apple"

#### Herramientas Útiles
- **Calculadora**: "calcula 15 + 30", "resuelve 100 / 4"
- **Traductor**: "traducir hola al inglés"
- **Recordatorios**: "recuérdame en 10 minutos revisar el horno"
- **Cronómetro**: "inicia timer", "detener cronómetro"
- **WhatsApp**: "envía whatsapp al +549123456789 Hola, ¿cómo estás?"

## Instalación

### Prerrequisitos
```bash
pip install pyttsx3 speech_recognition requests feedparser pyjokes pywhatkit yfinance wikipedia
```

### Archivos Necesarios
1. `asistenteVirtual.py` - Clase principal del asistente
2. `main.py` - Interfaz gráfica con Tkinter
3. `comandos.json` - Configuración de comandos

### Configuración de APIs
- **Clima**: API key de OpenWeatherMap incluida (puedes cambiarla en `_configurar_clima()`)
- **WhatsApp**: Requiere WhatsApp Web configurado

## Uso

### Ejecución
```bash
python main.py
```

### Interfaz
- **Campo de texto**: Escribe comandos manualmente
- **Botón "Enviar"**: Ejecuta el comando escrito
- **Botón "🎤 Escuchar"**: Activa/desactiva escucha continua
- **Consola**: Muestra el historial de conversaciones

### Ejemplos de Comandos
```
Usuario: "¿qué hora es?"
Asistente: "En este momento son las 14 horas con 30 minutos"

Usuario: "reproducir tango argentino"
Asistente: "Reproduciendo en YouTube..."

Usuario: "recuérdame en 5 minutos llamar a mamá"
Asistente: "De acuerdo, te recordaré en 5 minutos: llamar a mamá"
```

## Estructura del Proyecto

```
asistente-virtual/
├── asistenteVirtual.py    # Clase principal con toda la lógica
├── main.py                # Interfaz gráfica Tkinter
├── comandos.json          # Configuración de comandos
└── README.md             # Este archivo
```

## Personalización

### Agregar Nuevos Comandos
1. Crear el método en `AsistenteVirtual` clase: `comando_nuevo_comando(self, texto_completo)`
2. Agregar entrada en `comandos.json`:
```json
"nuevo_comando": {
  "keywords": ["palabra clave", "otra frase"],
  "funcion": "comando_nuevo_comando"
}
```

### Cambiar Voz
Modifica `_configurar_voz()` en `asistenteVirtual.py` para usar otra voz instalada en el sistema.

## Limitaciones
- Requiere conexión a internet para búsquedas, clima, noticias y traducciones
- El reconocimiento de voz puede verse afectado por ruido ambiente
- WhatsApp requiere configuración previa de WhatsApp Web

## Contribuir
Las mejoras son bienvenidas. Algunas ideas:
- Agregar más APIs (noticias locales, deportes, etc.)
- Mejorar la precisión del reconocimiento de voz
- Agregar más modismos argentinos
- Interfaz más moderna

## Licencia
Proyecto de código abierto para uso educativo y personal.