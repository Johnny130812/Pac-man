import tkinter as tk
import random
import os
import math

ruta_nuevo_directorio = "C:/Users/Jonny/Desktop/Proyecto"
os.chdir(ruta_nuevo_directorio)

matriz = [
    ['B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B'],
    ['N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N'],
    ['B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B'],
    ['N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N'],
    ['B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B'],
    ['N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N'],
    ['B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B'],
    ['N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N'],
    ['B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B'],
    ['N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N'],
    ['B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B'],
    ['N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N'],
    ['B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B'],
    ['N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N'],
    ['B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B', 'N', 'B']
]

tamano_celda = 33
espacio_entre_celdas = 12

ventana = tk.Tk()
ventana.geometry('1000x800')
ventana.configure(bg='black')

frame = tk.Frame(ventana)
frame.pack()

lienzo = tk.Canvas(frame, width=660, height=660, bg='black')
lienzo.grid(row=0, column=0)

def dibujar_celda(fila, columna):
    if fila < len(matriz) and columna < len(matriz[0]):
        x1 = columna * (tamano_celda + espacio_entre_celdas)
        y1 = fila * (tamano_celda + espacio_entre_celdas)
        x2 = x1 + tamano_celda
        y2 = y1 + tamano_celda
        valor = matriz[fila][columna]

        lienzo.create_rectangle(x1, y1, x2, y2, fill="white" if valor == 'B' else "black")
        # Llama a la función para dibujar la siguiente celda en la misma fila o avanza a la siguiente fila
        if columna + 1 < len(matriz[0]):
            dibujar_celda(fila, columna + 1)
        else:
            dibujar_celda(fila + 1, 0)

# Comienza la llamada recursiva para dibujar la matriz desde la primera celda (fila 0, columna 0)
dibujar_celda(0, 0)

# Carga una imagen para el jugador
imagen = tk.PhotoImage(file="bicho.gif")  
# Crea la imagen del jugador en el lienzo
jugador_id = lienzo.create_image(
    (len(matriz[0]) * tamano_celda + (len(matriz[0]) - 1) * espacio_entre_celdas) / 2,
    (len(matriz) - 1) * (tamano_celda + espacio_entre_celdas) + tamano_celda / 2,
    image=imagen
)

turno = 0
balas = []

# Función para verificar si dos objetos están lo suficientemente alejados
def esta_suficientemente_alejado(x1, y1, x2, y2, distancia_minima):
    return abs(x1 - x2) >= distancia_minima and abs(y1 - y2) >= distancia_minima

# Función para obtener las coordenadas de casillas blancas aleatorias en la parte superior
def obtener_casillas_blancas_superiores_aleatorias():
    casillas_blancas = [(fila, columna) for fila in range(len(matriz)) for columna in range(len(matriz[0])) if matriz[fila][columna] == 'B']
    casillas_superiores = [(fila, columna) for fila, columna in casillas_blancas if fila < len(matriz) // 2]
    return random.sample(casillas_superiores, 15)  # Selecciona 15 casillas aleatorias

# Variable para controlar si el jugador se movió en su turno
jugador_se_movio = False

# Función para mostrar un mensaje de "Game Over" y detener el juego
def game_over():
    lienzo.create_text(
        330, 330, text="Game Over", fill="red", font=("Arial", 36),
        anchor="center"
    )
    ventana.after_cancel(enemigo_movimiento)
    ventana.after_cancel(bala_movimiento)
    lienzo.unbind("<KeyPress>")  

# Variable global para el tiempo restante en segundos
tiempo_restante = 240  

# Etiqueta para mostrar el tiempo restante
tiempo_label = tk.Label(ventana, text=f"Tiempo restante: {tiempo_restante} s", bg='black', fg='white', font=("Arial", 14))
tiempo_label.place(relx=0.5, y=10, anchor="n")

# Función para actualizar el tiempo restante
def actualizar_tiempo():
    global tiempo_restante
    tiempo_restante -= 1
    tiempo_label.config(text=f"Tiempo restante: {tiempo_restante} s")

    if tiempo_restante <= 0:
        game_over()  # Llama a la función de "Game Over"
    else:
        ventana.after(1000, actualizar_tiempo)  # Programa una actualización cada segundo

# Llama a la función para iniciar el cronómetro
actualizar_tiempo()

# Función para cerrar el juego
def cerrar():
   ventana.destroy()

# Función para verificar si hay enemigos cerca de una casilla
def hay_enemigo_cerca(fila, columna):
    jugador_x, jugador_y = lienzo.coords(jugador_id)
    x = columna * (tamano_celda + espacio_entre_celdas)
    y = fila * (tamano_celda + espacio_entre_celdas)
    distancia_minima = tamano_celda + espacio_entre_celdas

    return any(esta_suficientemente_alejado(x, y, enemigo_x, enemigo_y, distancia_minima) for enemigo_x, enemigo_y in obtener_posiciones_enemigos())

# Función para obtener las posiciones de los enemigos
def obtener_posiciones_enemigos():
    enemigos_ids = lienzo.find_withtag("enemigo")
    return [(lienzo.coords(enemigo_id)) for enemigo_id in enemigos_ids]

# Crear un botón para cerrar el juego
boton_cerrar = tk.Button(ventana, text="cerrar", command=cerrar)
boton_cerrar.place(x=10, y=10)


# Función para mover a los enemigos
def mover_enemigo():
    global turno
    if turno == 1:  # Es el turno de los enemigos
        enemigos_ids = lienzo.find_withtag("enemigo")  # Obtiene los IDs de todos los enemigos

        if enemigos_ids:
            # Selecciona un enemigo aleatorio
            enemigo_id = random.choice(enemigos_ids)
            enemigo_x, enemigo_y = lienzo.coords(enemigo_id)

            jugador_x, jugador_y = lienzo.coords(jugador_id)

            # Calcula la dirección hacia la que el enemigo debe moverse para acercarse al jugador
            dx = jugador_x - enemigo_x
            dy = jugador_y - enemigo_y

            
            distancia = math.sqrt(dx**2 + dy**2)
            if distancia != 0:
                dx /= distancia
                dy /= distancia

            # Mueve al enemigo en la dirección calculada
            lienzo.move(enemigo_id, dx * (tamano_celda + espacio_entre_celdas), dy * (tamano_celda + espacio_entre_celdas))

            # Verifica si hay colisión con el jugador
            if lienzo.bbox(enemigo_id) and lienzo.bbox(jugador_id) and intersectan_bbox(lienzo.bbox(enemigo_id), lienzo.bbox(jugador_id)):
                game_over()  # Llama a la función de "Game Over"

            turno = 0  # Cambia el turno al jugador

enemigo_movimiento = ventana.after(1000, mover_enemigo)  # Inicia el movimiento de los enemigos

# Función para mover al jugador
def mover_jugador(event):
    global turno, jugador_se_movio, puntaje

    if turno == 0:  # Es el turno del jugador
        # Mueve la imagen en la dirección correspondiente al evento
        move_amount = tamano_celda + espacio_entre_celdas
        x, y = 0, 0

        jugador_x, jugador_y = lienzo.coords(jugador_id)

        if event.keysym == "Up":
            y = -move_amount
        elif event.keysym == "Down":
            y = move_amount
        elif event.keysym == "Left":
            x = -move_amount
        elif event.keysym == "Right":
            x = move_amount
        elif event.keysym == "1":  # Diagonal arriba izquierda
            x, y = -move_amount, -move_amount
        elif event.keysym == "2":  # Diagonal arriba derecha
            x, y = move_amount, -move_amount
        elif event.keysym == "q":  # Diagonal abajo izquierda
            x, y = -move_amount, move_amount
        elif event.keysym == "w":  # Diagonal abajo derecha
            x, y = move_amount, move_amount

        if x != 0 or y != 0:
            jugador_se_movio = True
            puntaje += 5  # Sumar 5 puntos al moverse
            puntaje_label.config(text=f"Puntaje: {puntaje}")

        # Mueve la imagen del jugador
        lienzo.move(jugador_id, x, y)
        turno = 1  # Cambia el turno a los enemigos
        mover_enemigo()

# Carga una imagen para los enemigos
imagen_enemigo = tk.PhotoImage(file="enemigo_2_.gif") 
# Función para crear enemigos en casillas blancas aleatorias en la parte superior
def crear_enemigos(casillas_blancas_superiores):
    if not casillas_blancas_superiores:
        return  # Si no quedan casillas, termina 

    fila, columna = casillas_blancas_superiores.pop(0)  # Obtiene la primera casilla y la elimina de la lista

    x = columna * (tamano_celda + espacio_entre_celdas)
    y = fila * (tamano_celda + espacio_entre_celdas)

    # Verifica que el enemigo esté lo suficientemente alejado del jugador
    jugador_x, jugador_y = lienzo.coords(jugador_id)
    if not esta_suficientemente_alejado(x, y, jugador_x, jugador_y, tamano_celda + espacio_entre_celdas):
        crear_enemigos(casillas_blancas_superiores)  # Llama para la siguiente casilla
        return

    # Crea la imagen del enemigo en el lienzo
    enemigo_id = lienzo.create_image(x + tamano_celda / 2, y + tamano_celda / 2, image=imagen_enemigo, tags="enemigo")

    # Llama para la siguiente casilla
    crear_enemigos(casillas_blancas_superiores)

# Llama a la función para crear enemigos pasando la lista de casillas blancas superiores aleatorias
casillas_blancas_superiores = obtener_casillas_blancas_superiores_aleatorias()
crear_enemigos(casillas_blancas_superiores) 

# Función para disparar balas
def disparar(event):
    x, y = lienzo.coords(jugador_id)

    if event.keysym == 'i':
        disparar_bala(x, y, 0, -1)  # Arriba
    elif event.keysym == 'k':
        disparar_bala(x, y, 0, 1)  # Abajo
    elif event.keysym == 'j':
        disparar_bala(x, y, -1, 0)  # Izquierda
    elif event.keysym == 'l':
        disparar_bala(x, y, 1, 0)  # Derecha
    elif event.keysym == 'o':
        disparar_bala(x, y, 1, -1)  # Diagonal arriba derecha
    elif event.keysym == 'u':
        disparar_bala(x, y, -1, -1)  # Diagonal arriba izquierda
    elif event.keysym == 'n':
        disparar_bala(x, y, -1, 1)  # Diagonal abajo izquierda
    elif event.keysym == 'm':
        disparar_bala(x, y, 1, 1)  # Diagonal abajo derecha

# Función para disparar una bala en una dirección específica
def disparar_bala(x, y, dx, dy):
    bala = lienzo.create_rectangle(x - 2, y - 20, x + 2, y - 10, fill="red")
    balas.append((bala, dx, dy, 90))  

# Función para mover las balas y eliminar enemigos cuando colisionan
def mover_balas():
    global puntaje

    balas_para_eliminar = []
    enemigos_para_eliminar = []  

    for i, (bala, dx, dy, pasos) in enumerate(balas):
        if pasos > 0:
            lienzo.move(bala, dx, dy)
            pasos -= 1
            balas[i] = (bala, dx, dy, pasos)
        else:
            balas_para_eliminar.append(i)

    # Verificar colisiones entre balas y enemigos
    for i, (bala, _, _, _) in enumerate(balas):
        bala_bbox = lienzo.bbox(bala)
        if bala_bbox:
            for enemigo_id in lienzo.find_withtag("enemigo"):
                enemigo_bbox = lienzo.bbox(enemigo_id)
                if enemigo_bbox and intersectan_bbox(bala_bbox, enemigo_bbox):
                    enemigos_para_eliminar.append(enemigo_id)
                    balas_para_eliminar.append(i)

    # Eliminar las balas que han alcanzado su límite de pasos
    for i in reversed(balas_para_eliminar):
        bala, _, _, _ = balas.pop(i)
        lienzo.delete(bala)

    # Eliminar enemigos que han sido alcanzados por balas
    for enemigo_id in enemigos_para_eliminar:
        lienzo.delete(enemigo_id)
        # Sumar 10 puntos cuando el jugador elimina un enemigo
        puntaje += 10
        puntaje_label.config(text=f"Puntaje: {puntaje}")

    lienzo.after(50, mover_balas)

bala_movimiento = mover_balas()  # Inicia el movimiento de las balas

def intersectan_bbox(bbox1, bbox2):
    x1_1, y1_1, x2_1, y2_1 = bbox1
    x1_2, y1_2, x2_2, y2_2 = bbox2
    return (x1_1 < x2_2 and x2_1 > x1_2 and y1_1 < y2_2 and y2_1 > y1_2)

balas = []

puntaje = 0

# Función para actualizar el puntaje
def actualizar_puntaje(puntos):
    global puntaje
    puntaje += puntos
    puntaje_label.config(text=f"Puntaje: {puntaje}")

# Crear un Label para mostrar el puntaje
puntaje_label = tk.Label(ventana, text=f"Puntaje: {puntaje}", bg='black', fg='white', font=("Arial", 14))
puntaje_label.place(relx=1, x=-10, y=10, anchor="ne")

# Función para manejar el teclado
def manejar_teclado(event):
    if event.keysym in ('Up', 'Down', 'Left', 'Right', 'space', 'i', 'o', 'l', 'k', 'j', 'u', 'n', 'm', '1', 'q', '2', 'w'):
        mover_jugador(event)  # Llamar a la función para mover al jugador
        disparar(event)  # Llamar a la función para disparar


ventana.bind("<KeyPress>", manejar_teclado)

# Coloca el foco en el lienzo para que pueda recibir eventos de teclado
lienzo.focus_set()

# Inicia la ventana de Tkinter
ventana.mainloop()
