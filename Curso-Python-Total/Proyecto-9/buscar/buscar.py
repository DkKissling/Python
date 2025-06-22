import os
import re
import time
from datetime import datetime

def buscar_numeros_de_serie(ruta):
    patron = r'N[a-zA-Z]{3}-\d{5}'
    resultados = []
    inicio = time.time()

    for carpeta, _, archivos in os.walk(ruta):
        for archivo in archivos:
            if archivo.endswith('.txt'):
                ruta_archivo = os.path.join(carpeta, archivo)
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    texto = f.read()
                    match = re.search(patron, texto)
                    if match:
                        resultados.append((archivo, match.group()))

    fin = time.time()
    duracion = round(fin - inicio)

    # Mostrar resultados
    fecha = datetime.today().strftime('%d/%m/%y')
    print("\n----------------------------------------------------")
    print(f"Fecha de búsqueda: {fecha}\n")
    print("ARCHIVO\t\tNRO. SERIE")
    print("-------\t\t-----------")
    for archivo, nro in resultados:
        print(f"{archivo}\t{nro}")
    print(f"\nNúmeros encontrados: {len(resultados)}")
    print(f"Duración de la búsqueda: {duracion} segundos")
    print("----------------------------------------------------\n")