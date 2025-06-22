# Importamos las librerías necesarias
import requests
from bs4 import BeautifulSoup

# URL del sitio web a hacer scraping (Books to Scrape es ideal para practicar)
url = "https://books.toscrape.com/"

# 1. Hacer una solicitud HTTP GET a la página
response = requests.get(url)

# Mostramos el código de estado de la respuesta (200 es éxito)
print("Código de estado:", response.status_code)

# 2. Crear el objeto BeautifulSoup para parsear el contenido HTML
soup = BeautifulSoup(response.text, 'html.parser')

# 3. Buscar elementos HTML específicos

# a) Buscar el primer título de un libro (etiqueta <h3>)
first_title = soup.find('h3')
print("Primer título:", first_title.text)  # Mostramos el texto del primer título

# b) Buscar todos los títulos de los libros (devuelve una lista de objetos)
all_titles = soup.find_all('h3')
print("Total de títulos encontrados:", len(all_titles))

# Mostramos los primeros 5 títulos encontrados
for i, title in enumerate(all_titles[:5]):
    print(f"{i+1}. {title.text})

# c) Buscar elementos por clase CSS: las calificaciones por estrellas
ratings = soup.find_all('p', class_='star-rating')
for rating in ratings[:5]:
    print("Clase de rating:", rating['class'])  # Ejemplo: ['star-rating', 'Three']

# d) Obtener el atributo 'href' de los links dentro de los títulos de libros
links = soup.select('h3 a')  # select() permite usar selectores CSS como en CSS puro
for link in links[:5]:
    href = link['href']  # Extraemos el valor del atributo href
    full_url = url + href  # Completamos la URL parcial con la base del sitio
    print("Link completo:", full_url)

# 4. Limpiar y procesar texto: por ejemplo, el precio del libro
raw_price = soup.find('p', class_='price_color').text  # Ej: '£51.77'
clean_price = raw_price.strip().replace('£', '')  # Quitamos símbolos y espacios
print("Precio limpio:", clean_price)

# 5. Navegar dentro del DOM: accedemos a elementos relacionados
book = soup.find('article', class_='product_pod')  # Cada libro está dentro de un <article>
title = book.h3.a['title']  # Título completo del libro desde el atributo 'title'
price = book.find('p', class_='price_color').text  # Precio del mismo libro
print(f"Título: {title}, Precio: {price}")
