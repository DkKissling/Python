# Importamos las librerías necesarias
import bs4                  # BeautifulSoup (bs4) se usa para analizar y navegar por el HTML
import requests             # requests se usa para hacer solicitudes HTTP

# URL base para acceder a cada página del catálogo
url_base = 'https://books.toscrape.com/catalogue/page-{}.html'

# Lista donde vamos a guardar los títulos con 4 o 5 estrellas
titulos_rating_alto = []

# Recorremos las 50 páginas del catálogo
for pagina in range(1, 51):

    # Creamos la URL para la página actual
    url_pagina = url_base.format(pagina)
    
    # Hacemos una solicitud HTTP GET a esa página
    resultado = requests.get(url_pagina)
    
    # Creamos un objeto BeautifulSoup para poder analizar el HTML
    sopa = bs4.BeautifulSoup(resultado.text, 'lxml')

    # Seleccionamos todos los libros en esa página (cada uno tiene la clase 'product_pod')
    libros = sopa.select('.product_pod')

    # Recorremos cada libro encontrado
    for libro in libros:

        # Verificamos si el libro tiene rating de 4 o 5 estrellas
        if len(libro.select('.star-rating.Four')) != 0 or len(libro.select('.star-rating.Five')) != 0:

            # Extraemos el título del libro desde el atributo 'title' del segundo <a> en el bloque
            titulo_libro = libro.select('a')[1]['title']

            # Guardamos el título en la lista
            titulos_rating_alto.append(titulo_libro)

# Imprimimos todos los títulos que tienen 4 o 5 estrellas
for t in titulos_rating_alto:
    print(t)
