import os

def recorrer_directorio(ruta):
    print(f"\nContenido del directorio: {ruta}\n")
    for carpeta, subcarpetas, archivos in os.walk(ruta):
        print(f"Carpeta: {carpeta}")
        print("Subcarpetas:")
        for sub in subcarpetas:
            print(f"\t{sub}")
        print("Archivos:")
        for arch in archivos:
            print(f"\t{arch}")
        print()
