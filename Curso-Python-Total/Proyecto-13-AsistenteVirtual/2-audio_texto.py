import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia



#escuchar nuetro microfono y dovolver el audio en texto 
def trasnformar_audio_en_texto():
    
    #almacenar el recognizer en variable
    r=sr.Recognizer()

    #configurar el microfono esta linea abre el microfono 
    #y lo que digas se asigna a la variable origen, y dice que todo lo que esta debaho 
    #de esta linea se ejecuta mientras el microfono esta abierto
    with sr.Microphone() as origen:
    
        #tiempo de espera
        r.pause_threshold=0.8

        #informar que comenzo la grabacion
        print("ya puedes hablar")

        #guardar lo que escuche como audio
        audio=r.listen(origen)

        try:
            #buscar en google lo que haya puesto en texto
            pedido = r.recognize_google(audio, language="es-AR")

            #prueba de que pudo ingresar niuestra voz en texto
            print("Dijiste: "+ pedido)

            #devolver pedido
            return pedido
        
        #En caso que no comprenda el audio 
        except sr.UnknownValueError:
            #Pruebba que no comprendio 
            print("ups, no entendi")

            return "Sigo esperando"
        
        #En caso de no resolver el pedido osea que si grabo el audio pero no puede convertilo en texto 

        except sr.RequestError:
            
            print("ups, no hay servicio")

            return "Sigo esperando"

        #Algun otro error
        except:
            print("ups,algo no a salido bien")

            return "Sigo esperando"

trasnformar_audio_en_texto()