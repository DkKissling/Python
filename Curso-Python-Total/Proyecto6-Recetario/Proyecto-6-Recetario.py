import os
from os import system
from pathlib import Path

RUTA = Path(r"C:\Users\usuario\Desktop\Curso Pyrhon Total\Proyecto6-Recetario\Recetas")

def mostrar_menu():
    print("\n" + "*" * 40)
    print("1. Leer receta")
    print("2. Crear receta nueva")
    print("3. Crear categoria nueva")
    print("4. Borrar receta")
    print("5. Borrar categoria")
    print("6. Salir")
    print("*" * 40 + "\n")

def contar_recetas():
    total = 0
    for categoria in os.listdir(RUTA):
        recetas = os.listdir(RUTA / categoria)
        total += len(recetas)
    return total

def listar_categorias():
    categorias = []
    for i, cat in enumerate(os.listdir(RUTA), 1):
        if os.path.isdir(RUTA / cat):
            print(f"{i}. {cat}")
            categorias.append(cat)
    return categorias

def elegir_categoria():
    print("\nCategorias disponibles:")
    cats = listar_categorias()
    try:
        opcion = int(input("Elige una categoria: "))
        return cats[opcion-1]
    except:
        print("Opcion no valida!")
        return None

def listar_recetas(categoria):
    print(f"\nRecetas en {categoria}:")
    recetas = os.listdir(RUTA / categoria)
    for i, rec in enumerate(recetas, 1):
        print(f"{i}. {rec}")
    return recetas

def elegir_receta(categoria):
    recetas = listar_recetas(categoria)
    try:
        opcion = int(input("Elige receta: "))
        return recetas[opcion-1]
    except:
        print("Opcion no valida!")
        return None

def leer_receta(categoria, receta):
    try:
        with open(RUTA / categoria / receta, 'r') as f:
            print("\n" + f.read())
    except:
        print("Error leyendo receta!")

def crear_receta(categoria):
    nombre = input("Nombre de la receta (ej: sopa.txt): ")
    contenido = input("Escribe la receta:\n")
    try:
        with open(RUTA / categoria / nombre, 'w') as f:
            f.write(contenido)
        print("Receta creada!")
    except:
        print("Error creando receta!")

def crear_categoria():
    nombre = input("Nombre de la nueva categoria: ")
    try:
        os.mkdir(RUTA / nombre)
        print("Categoria creada!")
    except:
        print("Error creando categoria!")

def borrar_receta(categoria):
    receta = elegir_receta(categoria)
    if receta:
        try:
            os.remove(RUTA / categoria / receta)
            print("Receta borrada!")
        except:
            print("Error borrando receta!")

def borrar_categoria(categoria):
    try:
        os.rmdir(RUTA / categoria)
        print("Categoria borrada!")
    except:
        print("Error borrando categoria!")

def main():
    print(f"Bienvenido al Recetario! ({contar_recetas()} recetas)")
    
    while True:
        mostrar_menu()
        opcion = input("Elige opcion: ")
        system("cls")
        
        if opcion == "1":
            cat = elegir_categoria()
            if cat:
                rec = elegir_receta(cat)
                if rec:
                    leer_receta(cat, rec)
                    input("\nPresiona Enter para continuar...")
        
        elif opcion == "2":
            cat = elegir_categoria()
            if cat:
                crear_receta(cat)
        
        elif opcion == "3":
            crear_categoria()
        
        elif opcion == "4":
            cat = elegir_categoria()
            if cat:
                borrar_receta(cat)
        
        elif opcion == "5":
            cat = elegir_categoria()
            if cat:
                borrar_categoria(cat)
        
        elif opcion == "6":
            print("Adios!")
            break
        
        else:
            print("Opcion no valida!")

if __name__ == "__main__":
    main()