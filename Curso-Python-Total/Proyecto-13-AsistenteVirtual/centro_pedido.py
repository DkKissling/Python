import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

id1 = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0'
id2 = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0'

def trasnformar_audio_en_texto():
    r = sr.Recognizer()
    with sr.Microphone() as origen:
        r.pause_threshold = 0.8
        try:
            audio = r.listen(origen, timeout=5, phrase_time_limit=10) 
            pedido = r.recognize_google(audio, language="es-AR")
            pedido = pedido.strip().lower()  
            return pedido
        except sr.UnknownValueError:
            print("Ups, no entendí.")
            return ""
        except sr.RequestError:
            print("Ups, no hay servicio.")
            return ""
        except:
            print("Ups, algo no ha salido bien.")
            return ""

def hablar(mensaje):
    engine = pyttsx3.init()
    engine.setProperty('voice', id1)
    engine.say(mensaje)
    engine.runAndWait()

def pedir_dia():
    dia = datetime.date.today()
    dia_semana = dia.weekday()
    calendario = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes', 5: 'Sábado', 6: 'Domingo'}
    hablar(f"Hoy es {calendario[dia_semana]} {dia.day} de {dia.month} de {dia.year}")

def pedir_hora():
    hora = datetime.datetime.now()
    mensaje = f"En este momento son las {hora.hour} horas con {hora.minute} minutos"
    hablar(mensaje)

def saludo_inicial():
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas Noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buenos Días'
    else:
        momento = 'Buenas Tardes'
    hablar(f'{momento}, soy tu asistente virtual. Por favor, dime en qué te puedo ayudar.')

def pedir_cosas():
    saludo_inicial()
    comenzar = True
    while comenzar:
        pedido = trasnformar_audio_en_texto()

        if pedido == "":
            hablar("No entendí. ¿Podés repetir?")
            continue

        if 'abrir youtube' in pedido:
            hablar('Con gusto, estoy abriendo YouTube')
            webbrowser.open('https://www.youtube.com/')
        elif 'abrir navegador' in pedido:
            hablar('Claro, estoy abriendo el navegador')
            webbrowser.open('https://www.google.com/')
        elif 'qué día es hoy' in pedido or 'decime el día' in pedido:
            pedir_dia()
        elif 'qué hora es' in pedido or 'decime la hora' in pedido:
            pedir_hora()
        elif 'cerrar programa' in pedido or 'salir' in pedido:
            hablar('Cerrando el programa. Hasta luego.')
            comenzar = False
        elif 'busca en wikipedia' in pedido:
            hablar('Buscando eso en wikipedia')
            pedido = pedido.replace('busca en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('Wikipedia dice lo siguiente:')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('Ya mismo estoy en eso')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
            continue
        elif 'reproducir' in pedido:
            hablar('Buena idea, ya comienzo a reproducirlo')
            pywhatkit.playonyt(pedido)
            continue
        elif 'broma' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple':'APPL',
                       'amazon':'AMZN',
                       'google':'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontré, el precio de {accion} es {precio_actual}')
                continue
            except:
                hablar("Perdón pero no la he encontrado")
                continue
        elif 'adiós' in pedido:
            hablar("Me voy a descansar, cualquier cosa me avisas")
            break

# Ejecutar el asistente
pedir_cosas()
