import os

def leer_instrucciones(ruta):
    for carpeta, _, archivos in os.walk(ruta):
        for archivo in archivos:
            if archivo.lower() == 'instrucciones.txt':
                ruta_archivo = os.path.join(carpeta, archivo)
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                    print("\nContenido de instrucciones.txt:\n")
                    print(contenido)
                return contenido
        break  
    print("No se encontró 'instrucciones.txt'.")
    return None
