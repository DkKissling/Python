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
        print("ya puedes hablar")
        audio = r.listen(origen)
        try:
            pedido = r.recognize_google(audio, language="es-AR")
            print("Dijiste: " + pedido)
            return pedido
        except sr.UnknownValueError:
            print("ups, no entendi")
            return "Sigo esperando"
        except sr.RequestError:
            print("ups, no hay servicio")
            return "Sigo esperando"
        except:
            print("ups,algo no a salido bien")
            return "Sigo esperando"

def hablar(mensaje):
    engine = pyttsx3.init()
    engine.setProperty('voice', id1)
    engine.say(mensaje)
    engine.runAndWait()

#informar que dia es
def pedir_dia():

    #crear variable con datos del dia
    dia = datetime.date.today()
    print(dia)
    #el numero de 1 al 7 con el dia correspondiente
    dia_semana = dia.weekday()
    print(dia_semana)

    #diccionario con los dias
    calendario={0: 'Lunes',1:'Martes',2:'Miércoles', 3:'Jueves', 4:'Viernes',5:'Sábado', 6:'Domingo'}

    #decir dia de la semana

    hablar(f"hoy es el dia {calendario[dia_semana]}")

#informar que hora es
def pedir_hora():

    #crear una variable con la hora
    hora=datetime.datetime.now()
    hora = f"En este momento son las {hora.hour} horas con {hora.minute} minutos"
    #decir la hora 
    hablar(hora)

#hacemos un saludo personalizado para que nos salude segun la hora y el dia
def saludo_inicial():
    hora=datetime.datetime.now()

#   CONDICION PARA SABERL EL HORARIO
    if hora.hour<6 or hora.hour>20:
        momento='Buenas Noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buenos Dias'
    else:
        momento ='Buenas Tardes'

    hablar(f'{momento} soy tu asistente virtual. Porfavor dime en que te puedo ayudar')

saludo_inicial()
pedir_dia()
pedir_hora()