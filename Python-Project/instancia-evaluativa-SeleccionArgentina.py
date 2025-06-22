Dadas cuatro listas que contienen los nombres de los jugadores de un equipo de fútbol, clasificados por posición (arqueros, defensores, mediocampistas y delanteros), y una lista adicional que indica la procedencia y posición de cada jugador (local o extranjero, y su posición en el campo), realiza las siguientes tareas:

Imprime los nombres de los jugadores titulares del equipo.
Crea una lista con los nombres de los jugadores locales que son arqueros o delanteros titulares.
Imprime los nombres de los jugadores locales que no son mediocampistas.

Ten en cuenta que en las listas de jugadores, los nombres de los titulares están seguidos de '(T)'

# Lista de jugadores por posición
Arqueros = ["Sergio Romero", "Wilfredo Caballero", "Nahuel Guzmán", "Franco Armani(T)"]
Defensores = ["Eduardo Salvio", "Gabriel Mercado(T)", "Nicolás Otamendi(T)", "Javier Mascherano", "Federico Fazio", "Marcos Rojo", "Marcos Acuña", "Ramiro Funes Mori", "Germán Pezzella(T)", "Cristian Ansaldi", "Nicolás Tagliafico(T)"]
Mediocampistas = ["Lucas Biglia", "Ever Banega", "Giovani Lo Celso(T)", "Manuel Lanzini", "Enzo Perez", "Pablo Perez", "Leandro Paredes(T)", "Guido Pizarro", "Rodrigo Battaglia", "Ricardo Centurión(T)", "Angel Di María", "Diego Perotti", "Maximiliano Meza"]
Delanteros = ["Paulo Dybala", "Sergio Agüero", "Gonzalo Higuaín", "Lionel Messi(T)", "Mauro Icardi", "Lautaro Martínez(T)", "Cristian Pavón(T)"]

# Procedencia y posición de los jugadores
procYpos = ["e-arq", "e-arq","e-arq", "l-arq", "e-def","e-def","e-def","e-def","e-def","e-def","e-def","e-def","e-def","e-def","e-def","e-vol","e-vol","e-vol","e-vol","l-vol", "l-vol", "e-vol","e-vol",
"e-vol","l-vol", "e-vol","e-vol","l-vol", "e-del","e-del","e-del","e-del","e-del","l-del", "l-del"]

# Combinar todas las listas de jugadores
jugadores = Arqueros + Defensores + Mediocampistas + Delanteros

# Lista para almacenar los jugadores locales (arqueros y delanteros titulares)
locales = []

# Imprimir el equipo titular
print("El equipo titular es:")
for i in range(len(jugadores)):
    x = jugadores[i].find("(T)")
    y = jugadores[i].find(" ")
    if x > 0: 
        # Extraer el nombre del jugador titular
        titular = jugadores[i][y:x]
        print(titular) # Imprimir el nombre del jugador titular
    
    # Agregar jugadores locales (arqueros y delanteros) a la lista
    if procYpos[i] == "l-arq" or procYpos[i] == "l-del":
        locales.append(jugadores[i][y:x])

# Imprimir los locales que no son mediocampistas
print("Locales que no son mediocampistas:")
for i in range(len(locales)):
    print(locales[i]) # Imprimir el nombre del local que no es mediocampista

