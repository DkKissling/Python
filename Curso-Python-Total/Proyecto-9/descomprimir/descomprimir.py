import shutil

def descomprimir_archivo(archivo_zip, destino):
    shutil.unpack_archive(archivo_zip, destino, "zip")
    print(f"Archivo '{archivo_zip}' descomprimido en '{destino}'.")