from descomprimir.descomprimir import descomprimir_archivo
from recorrer.recorrer import recorrer_directorio
from leer.leer import leer_instrucciones
from buscar.buscar import buscar_numeros_de_serie

def main():
    zip_path = 'Proyecto+Dia+9.zip'
    carpeta_destino = 'Proyecto+Dia+9+descomprimido'
    ruta_completa = 'C:\\Users\\usuario\\Desktop\\Curso Pyrhon Total\\Proyecto-9\\' + carpeta_destino

    descomprimir_archivo(zip_path, ruta_completa)
    recorrer_directorio(ruta_completa)
    leer_instrucciones(ruta_completa)
    buscar_numeros_de_serie(ruta_completa)

if __name__ == '__main__':
    main()
