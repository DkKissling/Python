import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

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

#funcion para que el asistente pueda ser escuchado

def hablar(mensaje):

    #encender motor de pyttsxx3
    engine=pyttsx3.init()

    #darle una vvoz distinta 
    engine.setProperty('voice',id1)

    #pronunciar mensaje
    #say lo pone en cola de frase por pronunciar 
    #runAndWait dice ahora si reproducilo
    engine.say(mensaje)
    engine.runAndWait()

#estos id son los tipos de voccces que tiene la maquina para hablar, en ingles o español
id1='HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0'
id2='HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'

hablar("what append?")