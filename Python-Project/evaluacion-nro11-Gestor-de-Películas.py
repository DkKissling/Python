Crea un sistema de gestión de información sobre películas. El programa debe extraer información de un archivo JSON que contiene datos sobre películas, como título, actores, calificación y recaudación, y guardar esta información en un archivo de texto. Luego, presenta un menú interactivo que permite al usuario seleccionar una película y ver detalles como el título, los actores, la calificación promedio o la recaudación total. Utiliza una clase Pelicula para extraer y guardar la información, y otra clase Menu para mostrar las opciones al usuario y procesar su selección.

class Pelicula:
    def extraer_guardar_informacion(self):
        # Lectura del archivo JSON
        with open("pelis.json", "r", encoding="utf8") as archivo:
            data = archivo.read()

        # Inicialización de listas para almacenar la información
        films = []
        actors = []
        ratings = []
        recaudaciones = []

        # División del archivo y extracción de información
        for x in range(1, 16):
            inicio = (x - 1) * 15
            parte = data[inicio:inicio + 15]

            title_index = parte.find('Title')
            actor_index = parte.find('Actors')
            rating_index = parte.find('Rotten Tomato')
            recaudacion_index = parte.find('BoxOffice')

            if title_index != -1:
                corte = parte.find("Year")
                titulo = parte[title_index + 8:corte].replace('"', '').replace(',', '').strip()
                films.append(titulo)
            elif actor_index != -1:
                corte = parte.find('Plot')
                actor = parte[actor_index + 9:corte].replace('"', '').split(',')[0].strip()
                actors.append(actor)
            elif rating_index != -1:
                corte = parte.find('%"')
                rating_value = parte[rating_index + 42:corte].replace('"', '').strip()
                ratings.append(rating_value)
            elif recaudacion_index != -1:
                corte = parte.find('Production')
                recaudacion = parte[recaudacion_index + 13:corte].replace('"', '').replace('$', '').replace(',', '').strip()
                recaudaciones.append(recaudacion)

        # Escritura de la información en un archivo de texto
        with open('pelis.txt', 'w', encoding='utf8') as archivo_txt:
            for i in range(min(3, len(films))):
                archivo_txt.write(f'Título: {films[i]}\nActor: {actors[i]}\nRating: {ratings[i]}\nRecaudación: {recaudaciones[i]}\n')


class Menu:
    def mostrar_opciones(self):
        # Lectura del archivo de texto
        with open("pelis.txt", "r", encoding="utf8") as archivo_txt:
            texto = archivo_txt.read()

        # Procesamiento del contenido
        lista = texto.split('\n')

        # Mostrar opciones al usuario
        print("Bienvenido")
        print("Utilice los números para elegir su opción", '\n')
        print("1- Arrival")
        print("2- Transcendence")
        print("3- Serenity")
        print("4- Ver rating promedio")
        print("5- Ver la recaudación total",'\n')

        # Interacción con el usuario
        while True:
            try:
                opcion = int(input("¿Cuál es su opción? "))
                if 1 <= opcion <= 5:
                    if opcion in range(1, 4):
                        inicio = (opcion - 1) * 4
                        fin = inicio + 4
                        print('\n'.join(lista[inicio:fin]))
                    elif opcion == 4:
                        ratings = [int(num) for num in texto.split() if num.isdigit()]
                        promedio = sum(ratings) / len(ratings)
                        print(f"El rating promedio es: {promedio}")
                    elif opcion == 5:
                        recaudaciones = [int(num) for num in texto.split() if num.isdigit()]
                        total = sum(recaudaciones)
                        print(f"La recaudación total es: {total}")
                    break
                else:
                    print("No es una opción válida")
            except ValueError:
                print("No es una opción válida")


# Ejecución del programa
if __name__ == "__main__":
    pelicula = Pelicula()
    pelicula.extraer_guardar_informacion()
    
    menu = Menu()
    menu.mostrar_opciones()

