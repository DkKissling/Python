import json
import threading
import time
import re
import datetime
import webbrowser
import requests
import feedparser
import pyttsx3
import speech_recognition as sr
import wikipedia
import pyjokes
import pywhatkit
import yfinance as yf


class AsistenteVirtual:
    """Clase principal del Asistente Virtual. Maneja el reconocimiento de voz, síntesis de voz y ejecución de comandos."""
    
    def __init__(self, path_json_comandos="comandos.json"):
        # === CONFIGURACIÓN DE VOZ ===
        self._configurar_voz()
        
        # === CARGAR COMANDOS DESDE JSON ===
        self._cargar_comandos(path_json_comandos)
        
        # === CONFIGURACIONES ADICIONALES ===
        self._configurar_recordatorios()
        self._configurar_clima()
    
    # ===================================================================
    # MÉTODOS DE CONFIGURACIÓN (se ejecutan al inicializar)
    # ===================================================================
    
    def _configurar_voz(self):
        """Configura el motor de texto a voz en español."""
        self.voz_id = (
            'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\'
            'Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0'
        )
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', self.voz_id)
    
    def _cargar_comandos(self, path_json_comandos):
        with open(path_json_comandos, "r", encoding="utf-8") as f:
            self.comandos_data = json.load(f)
    
    def _configurar_recordatorios(self):
        """Inicializa las listas para manejar recordatorios y timers."""
        self.recordatorios_activos = []   
        self.timers_activos = {}          
    
    def _configurar_clima(self):
        """Configura la API key para consultar el clima."""
        self.owm_api_key = "bb4b1caab71c031896bad676bc80f8a9"
    
    # ===================================================================
    # MÉTODOS BÁSICOS DE VOZ Y RECONOCIMIENTO
    # ===================================================================
    
    def hablar(self, mensaje):
        """
        Convierte texto a voz y lo reproduce.mensaje (str): El texto que el asistente dirá
        """
        self.engine.say(mensaje)
        self.engine.runAndWait()
    
    def transformar_audio_en_texto(self):
        """
        Escucha por el micrófono y convierte el audio a texto.El texto reconocido en minúsculas, o cadena vacía si no entiende
        """
        r = sr.Recognizer()
        with sr.Microphone() as origen:
            r.pause_threshold = 1.8  # Pausa antes de considerar que terminó de hablar
            try:
                # Escuchar con timeout de 5 segundos
                audio = r.listen(origen, timeout=5, phrase_time_limit=20)
                texto = r.recognize_google(audio, language="es-AR")
                return texto.strip().lower()
            except (sr.UnknownValueError, sr.RequestError):
                return ""  # Si no entiende o hay error, devuelve cadena vacía
    
    # ===================================================================
    # COMANDOS BÁSICOS (fecha, hora, saludo)
    # ===================================================================
    
    def saludo_inicial(self):
        hora_actual = datetime.datetime.now().hour
        
        if hora_actual < 6 or hora_actual > 20:
            saludo = "Buenas Noches"
        elif hora_actual < 13:
            saludo = "Buenos Días"
        else:
            saludo = "Buenas Tardes"
        
        self.hablar(f"{saludo}, soy tu asistente virtual. ¿En qué puedo ayudarte?")
    
    def comando_pedir_dia(self, _texto_completo=None):
        hoy = datetime.date.today()
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        
        dia_nombre = dias_semana[hoy.weekday()]
        self.hablar(f"Hoy es {dia_nombre} {hoy.day} de {hoy.month} de {hoy.year}")
    
    def comando_pedir_hora(self, _texto_completo=None):
        ahora = datetime.datetime.now()
        self.hablar(f"En este momento son las {ahora.hour} horas con {ahora.minute} minutos")
    
    # ===================================================================
    # COMANDOS DE NAVEGACIÓN WEB
    # ===================================================================
    
    def comando_abrir_youtube(self, _texto_completo=None):
        self.hablar("Con gusto, abriendo YouTube")
        webbrowser.open("https://www.youtube.com/")
    
    def comando_abrir_navegador(self, _texto_completo=None):
        self.hablar("Claro, abriendo el navegador")
        webbrowser.open("https://www.google.com/")
    
    # ===================================================================
    # COMANDOS DE ENTRETENIMIENTO
    # ===================================================================
    
    def comando_contar_broma(self, _texto_completo=None):
        chiste = pyjokes.get_joke("es")
        self.hablar(chiste)
    
    # ===================================================================
    # COMANDOS DE BÚSQUEDA
    # ===================================================================
    
    def comando_buscar_wikipedia(self, texto_completo):
        """
        Ejemplo: 'busca en wikipedia Python'
        """
        # Extraer el término de búsqueda removiendo las palabras clave
        termino = self._extraer_termino_busqueda(texto_completo, "buscar_wikipedia")
        
        if not termino:
            self.hablar("No especificaste lo que quieres buscar en Wikipedia.")
            return
        
        self.hablar("Buscando en Wikipedia...")
        wikipedia.set_lang("es")
        
        try:
            resumen = wikipedia.summary(termino, sentences=1)
            self.hablar("Wikipedia dice lo siguiente:")
            self.hablar(resumen)
        except Exception:
            self.hablar("No encontré resultados en Wikipedia.")
    
    def comando_buscar_internet(self, texto_completo):
        """
        Ejemplo: 'busca en internet recetas de pizza'
        """
        termino = self._extraer_termino_busqueda(texto_completo, "buscar_internet")
        
        if not termino:
            self.hablar("No me dijiste qué buscar en Internet.")
            return
        
        self.hablar("Buscando en Internet...")
        pywhatkit.search(termino)
        self.hablar("Esto es lo que encontré.")
    
    def comando_reproducir_youtube(self, texto_completo):
        """
        Ejemplo: 'reproducir música de rock'
        """
        termino = self._extraer_termino_busqueda(texto_completo, "reproducir_youtube")
        
        if not termino:
            self.hablar("No especificaste qué quieres reproducir en YouTube.")
            return
        
        self.hablar("Reproduciendo en YouTube...")
        pywhatkit.playonyt(termino)
    
    # ===================================================================
    # COMANDOS FINANCIEROS
    # ===================================================================
    
    def comando_precio_accion(self, texto_completo):
        """
        Ejemplo: 'precio de las acciones de Apple'
        """
        # Empresas disponibles (se puede expandir)
        empresas_disponibles = {
            "apple": "AAPL",
            "amazon": "AMZN", 
            "google": "GOOGL"
        }
        
        # Buscar si alguna empresa está mencionada en el texto
        empresa_encontrada = None
        ticker_symbol = None
        
        for empresa, ticker in empresas_disponibles.items():
            if empresa in texto_completo.lower():
                empresa_encontrada = empresa
                ticker_symbol = ticker
                break
        
        if not empresa_encontrada:
            self.hablar("¿Qué acción quieres saber su precio? Puedo consultar Apple, Amazon o Google.")
            return
        
        precio = self._obtener_precio_accion(ticker_symbol)
        
        if precio:
            self.hablar(f"El precio de {empresa_encontrada.capitalize()} es {precio} dólares.")
        else:
            self.hablar("No pude obtener el precio de la acción.")
    
    def _obtener_precio_accion(self, ticker_symbol):
        try:
            ticker_obj = yf.Ticker(ticker_symbol)
            precio = ticker_obj.info.get("regularMarketPrice")
            return precio
        except:
            return None
    
    # ===================================================================
    # COMANDOS DE CLIMA
    # ===================================================================
    
    def comando_clima(self, texto_completo):
        """
        Ejemplo: '¿qué tiempo hace en Madrid?'
        """
        ciudad = self._extraer_termino_busqueda(texto_completo, "clima")
        
        if not ciudad:
            self.hablar("¿En qué ciudad quieres saber el clima?")
            return
        
        clima_info = self._consultar_clima(ciudad)
        if clima_info:
            temp, descripcion = clima_info
            self.hablar(f"En {ciudad} hace {descripcion} con {temp}°C.")
        else:
            self.hablar("Lo siento, no pude obtener el clima en este momento.")
    
    def _consultar_clima(self, ciudad):
        """Consulta el clima usando la API de OpenWeatherMap."""
        url = (
            f"http://api.openweathermap.org/data/2.5/weather"
            f"?q={ciudad}&appid={self.owm_api_key}&units=metric&lang=es"
        )
        
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            
            if data.get("cod") != 200:
                return None
            
            temperatura = data["main"]["temp"]
            descripcion = data["weather"][0]["description"]
            return temperatura, descripcion
        except Exception:
            return None
    
    # ===================================================================
    # COMANDOS DE RECORDATORIOS Y TIMERS
    # ===================================================================
    
    def comando_recordatorio(self, texto_completo):
        """
        Ejemplo: 'recuérdame en 10 minutos que revise el horno'
        """
        # Buscar patrón: "recuérdame en X minutos que..."
        match = re.search(
            r"(?:recuérdame en|recordarme en)\s+(\d+)\s+minutos?\s+(.*)",
            texto_completo
        )
        
        if not match:
            self.hablar("No entendí el tiempo del recordatorio. "
                       "Debe ser algo como 'recuérdame en 10 minutos ...'.")
            return
        
        minutos = int(match.group(1))
        mensaje_recordatorio = match.group(2).strip()
        
        # Crear recordatorio en hilo separado
        self._crear_recordatorio(minutos, mensaje_recordatorio)
        self.hablar(f"De acuerdo, te recordaré en {minutos} minutos: {mensaje_recordatorio}")
    
    def _crear_recordatorio(self, minutos, mensaje):
        """Crea un recordatorio que se ejecuta en un hilo separado."""
        def alarma():
            time.sleep(minutos * 60)  # Convertir minutos a segundos
            self.hablar(f"Recordatorio: {mensaje}")
        
        hilo = threading.Thread(target=alarma)
        hilo.daemon = True  # Se cierra cuando se cierra el programa principal
        hilo.start()
        self.recordatorios_activos.append(hilo)
    
    def comando_timer(self, texto_completo):
        """
        Maneja cronómetros: iniciar, consultar tiempo, detener.
        Ejemplos: 'inicia timer', 'detener cronómetro'
        """
        if "detener" in texto_completo:
            self._detener_timer()
        else:
            self._iniciar_o_consultar_timer()
    
    def _iniciar_o_consultar_timer(self):
        if "principal" not in self.timers_activos:
            # Iniciar nuevo timer
            self.timers_activos["principal"] = time.time()
            self.hablar("Cronómetro iniciado.")
        else:
            # Consultar tiempo transcurrido
            tiempo_transcurrido = time.time() - self.timers_activos["principal"]
            minutos = int(tiempo_transcurrido // 60)
            segundos = int(tiempo_transcurrido % 60)
            self.hablar(f"El cronómetro lleva {minutos} minutos y {segundos} segundos.")
    
    def _detener_timer(self):
        if "principal" in self.timers_activos:
            tiempo_transcurrido = time.time() - self.timers_activos["principal"]
            minutos = int(tiempo_transcurrido // 60)
            segundos = int(tiempo_transcurrido % 60)
            self.hablar(f"Cronómetro detenido en {minutos} minutos y {segundos} segundos.")
            del self.timers_activos["principal"]
        else:
            self.hablar("No hay ningún cronómetro activo.")
    
    # ===================================================================
    # COMANDOS DE UTILIDADES
    # ===================================================================
    
    def comando_calculadora(self, texto_completo):
        """
        Ejemplos: 'calcula 2 + 2 * 3', 'resuelve 15 / 3'
        """
        expresion = self._extraer_termino_busqueda(texto_completo, "calculadora")
        
        if not expresion:
            self.hablar("¿Qué operación quieres calcular?")
            return
        
        try:
            # ADVERTENCIA: eval puede ser peligroso, se limita el contexto
            resultado = eval(expresion, {"__builtins__": {}})
            self.hablar(f"El resultado de {expresion} es {resultado}")
        except Exception:
            self.hablar("No pude calcular esa expresión. Revisa la sintaxis.")
    
    def comando_noticias(self, _texto_completo=None):
        """Obtiene las últimas noticias de BBC Mundo."""
        self.hablar("Obteniendo las últimas noticias...")
        
        noticias = self._obtener_noticias()
        if noticias:
            self.hablar("Estas son las últimas noticias:")
            for noticia in noticias[:3]:  # Solo las primeras 3
                self.hablar(noticia)
        else:
            self.hablar("No pude obtener las noticias ahora mismo.")
    
    def _obtener_noticias(self):
        """Obtiene noticias del RSS de BBC Mundo."""
        rss_url = "http://feeds.bbci.co.uk/mundo/rss.xml"
        try:
            feed = feedparser.parse(rss_url)
            if not feed.entries:
                return None
            return [entrada.title for entrada in feed.entries]
        except Exception:
            return None
    
    def comando_traducir(self, texto_completo):
        """Ejemplo: 'traducir hola al inglés'"""
        # Mapeo de idiomas soportados
        idiomas_soportados = {
            "inglés":    "es|en",
            "ingles":    "es|en",
            "español":   "es|en",   
            "francés":   "es|fr",
            "frances":   "es|fr",
            "alemán":    "es|de",
            "aleman":    "es|de",
            "portugués": "es|pt",
            "portugues": "es|pt"
        } #Con o sin acentos por las dudas
        
        # Buscar patrón más flexible: puede ser "traducir TEXTO al IDIOMA" o "traducir TEXTO a IDIOMA"
        match = re.search(r"(?:traducir|traduce)\s+(.*?)\s+(?:al?\s+)(\w+)", texto_completo)
        if not match:
            self.hablar("Formato incorrecto. Di algo como 'traducir hola al inglés' o 'traducir buenos días a francés'.")
            return
        
        texto_a_traducir = match.group(1).strip()
        idioma_destino = match.group(2).strip().lower()
        
        # Verificar si el idioma es soportado
        if idioma_destino not in idiomas_soportados:
            idiomas_disponibles = ", ".join(set(idiomas_soportados.keys()))
            self.hablar(f"No conozco el idioma {idioma_destino}. Idiomas disponibles: {idiomas_disponibles}.")
            return
        
        # Realizar la traducción
        langpair = idiomas_soportados[idioma_destino]
        traduccion = self._traducir_texto(texto_a_traducir, langpair)
        
        if traduccion:
            self.hablar(f"Traducción: {traduccion}")
        else:
            self.hablar("Error al traducir. Intenta más tarde.")
    
    def _traducir_texto(self, texto, langpair):
        """Traduce texto usando la API de MyMemory."""
        # Llamar a la API
        texto_url = requests.utils.quote(texto)
        url = f"https://api.mymemory.translated.net/get?q={texto_url}&langpair={langpair}"
        
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            return data.get("responseData", {}).get("translatedText", "")
        except Exception:
            return None
    
    def comando_whatsapp(self, texto_completo):
        """
        Ejemplo: 'envía whatsapp al +34123456789 Hola, ¿cómo estás?'
        """
        match = re.search(r"whatsapp\s+(?:al\s+)?(\+?\d+)\s+(.*)", texto_completo)
        if not match:
            self.hablar("Di algo como 'envía whatsapp al +34123456789 Tu mensaje aquí'.")
            return
        
        numero = match.group(1)
        mensaje = match.group(2).strip()
        
        if self._enviar_whatsapp(numero, mensaje):
            self.hablar(f"Enviando WhatsApp a {numero} en un minuto.")
        else:
            self.hablar("No pude enviar el WhatsApp. Verifica el número y tu conexión.")
    
    def _enviar_whatsapp(self, numero, mensaje):
        """Envía un mensaje de WhatsApp usando pywhatkit."""
        try:
            # Programar envío para dentro de 1 minuto
            now = datetime.datetime.now() + datetime.timedelta(minutes=1)
            pywhatkit.sendwhatmsg(numero, mensaje, now.hour, now.minute)
            return True
        except Exception:
            return False
    
    def comando_cerrar(self, _texto_completo=None):
        """Cierra el programa."""
        self.hablar("Cerrando el programa. ¡Hasta luego!")
        raise SystemExit
    
    # ===================================================================
    # MÉTODOS AUXILIARES
    # ===================================================================
    
    def _extraer_termino_busqueda(self, texto_completo, tipo_comando):
        """
        Extrae el término de búsqueda removiendo las palabras clave del comando.
        Args:
            texto_completo (str): El texto completo del usuario
            tipo_comando (str): El tipo de comando (clave en comandos_data)
        Returns:
            str: El término de búsqueda limpio
        """
        termino = texto_completo
        palabras_clave = self.comandos_data[tipo_comando]["keywords"]
        
        for palabra_clave in palabras_clave:
            if palabra_clave in texto_completo:
                termino = texto_completo.replace(palabra_clave, "").strip()
                break
        
        return termino
    
    # ===================================================================
    # MÉTODO PRINCIPAL DE EJECUCIÓN
    # ===================================================================
    
    def ejecutar_comando(self, texto_usuario):
        """
        Busca y ejecuta el comando correspondiente al texto del usuario.
        Args:
            texto_usuario (str): Lo que dijo o escribió el usuario
        Returns:
            bool: True si encontró y ejecutó un comando, False si no
        """
        # Recorrer todos los comandos disponibles
        for id_comando, info_comando in self.comandos_data.items():
            nombre_funcion = info_comando.get("funcion")
            palabras_clave = info_comando.get("keywords", [])
            
            # Verificar si alguna palabra clave esta en el texto del usuario
            for palabra_clave in palabras_clave:
                if palabra_clave in texto_usuario:
                    # Buscar el método correspondiente en la clase
                    metodo = getattr(self, nombre_funcion, None)
                    
                    if callable(metodo):
                        try:
                            metodo(texto_usuario)
                            return True  # Comando ejecutado exitosamente
                        except SystemExit:
                            raise  # Permitir que SystemExit se propague para cerrar
        
        return False  # No se encontró ningún comando
    
    def iniciar(self):
        """
        Bucle principal del asistente.
        Saluda al usuario y escucha comandos hasta que se le diga que se cierre.
        """
        self.saludo_inicial()
        
        while True:
            # Escuchar comando por voz
            comando_reconocido = self.transformar_audio_en_texto()
            
            if not comando_reconocido:
                self.hablar("No entendí, ¿podés repetir?")
                continue
            
            try:
                # Intentar ejecutar el comando
                comando_encontrado = self.ejecutar_comando(comando_reconocido)
                
                if not comando_encontrado:
                    self.hablar("Lo siento, no sé cómo responder a eso.")
                    
            except SystemExit:
                # Si el usuario dijo "cerrar" o "salir", terminar el programa
                break