import tkinter as tk
from tkinter import Scale
import pygame
from PIL import Image, ImageTk
import os
import subprocess


pygame.init()

# Cambiar al directorio deseado
# Esto es porque me tiraba a otro directorio y no ejecutaba bien jajaja
ruta_nuevo_directorio = "C:/Users/Jonny/Desktop/Pac-man"
os.chdir(ruta_nuevo_directorio)

#Ventana principal
ventana_principal = tk.Tk()
ventana_principal.configure(bg='midnight blue')
ventana_principal.geometry('700x600')
#Para no poder maximizar la ventana
ventana_principal.resizable(False, False)

#Función del botón about
def about():

    global foto
    ventana_about = tk.Toplevel()
    ventana_about.configure(bg='black')
    ventana_about.geometry('700x600')
    ventana_about.resizable(False, False)

#Ventana del juego
def juego():
    #El juego está en un archivo aparte, uso la biblioteca subprocess para llamarlo y ejecutarlo desde acá
    subprocess.run(["python", "main2.py"])
    

def ayuda():
    ventana = tk.Toplevel()
    ventana.configure(bg='black')
    ventana.geometry('700x600')
    

def configuracion():
    ventana_config = tk.Toplevel()
    ventana_config.configure(bg='black')
    ventana_config.geometry('700x600')

    def ajustar_volumen(valor):
        pygame.mixer.music.set_volume(float(valor) / 100)

    etiqueta_volumen = tk.Label(ventana_config, text="Volumen de la música:", bg='black', fg='yellow', font=fuente_creditos)
    etiqueta_volumen.pack()
    slider_volumen = Scale(ventana_config, from_=0, to=100, orient="horizontal", length=300, command=ajustar_volumen, bg=color1, font=fuente_botones)
    slider_volumen.pack()    

#Ventana del login
def login():
    ventana_login = tk.Toplevel()
    ventana_login.configure(bg='black')
    ventana_login.geometry('500x300')
    ventana_login.resizable(False,False)

    label_login = tk.Label(ventana_login, text='Inserte nombre de usuario', bg='black', font=fuente_creditos, fg='yellow')
    label_login.pack()
    usuario = tk.Entry(ventana_login, font=fuente_botones)
    usuario.pack(pady=10)

    def guardar_y_abrir(): 
        nombre = usuario.get()
        if nombre:
            with open('puntajes-.txt', 'a') as archivo:
                archivo.write(nombre + '\n')
            ventana_login.destroy() #Se destruye la ventana para pasar al juego
            juego()
        else:
            print('ERROR') #Se imprime por consola si hay algún error

    btn_login = tk.Button(ventana_login, bg=color1, font=fuente_botones, text='Jugar', borderwidth=10, command=guardar_y_abrir)
    btn_login.pack(pady=20)

    # Botón para volver
    btn_volver = tk.Button(ventana_login, bg=color1, font=fuente_creditos, text='X', borderwidth=10, command=ventana_login.destroy)
    btn_volver.place(x=5, y=118)

def puntajes():
    ventana_puntajes = tk.Toplevel()
    ventana_puntajes.configure(bg='black')
    ventana_puntajes.geometry('500x200')

     # Leer nombres desde el archivo "puntajes-.txt"
    with open('puntajes-.txt', 'r') as archivo:
        nombres = sorted(archivo.readlines())

    # Crear una etiqueta para mostrar los nombres
    nombres_label = tk.Label(ventana_puntajes, text="Salón de la fama:", bg='black', fg='yellow', font=fuente_creditos)
    nombres_label.pack()

    # Función para mostrar nombres
    def mostrar_nombre(indice):
        if indice < len(nombres):
            nombre_label = tk.Label(ventana_puntajes, text=nombres[indice].strip(), bg='black', fg='yellow', font=fuente_creditos)
            nombre_label.pack()
            ventana_puntajes.after(1000, mostrar_nombre, indice + 1)  # Mostrar el siguiente nombre después de 1 segundo

    # Iniciar la función con el primer índice (0)
    mostrar_nombre(0)
    
    
#Música de menú
pygame.mixer.init()
pygame.mixer.music.load("theme.mp3")
pygame.mixer.music.play(-1) #Para que la música esté en bucle

#Fuente de los botones
fuente_botones = ('8BIT WONDER Nominal', 20)
fuente_creditos = ('8BIT WONDER Nominal', 15)

#Botones
boton_start = tk.Button(ventana_principal, bg='midnight blue', text='Iniciar', width=19, fg='white', font=fuente_botones, command=login,)
boton_start.place(x=85, y=170)

boton_puntajes = tk.Button(ventana_principal, bg='midnight blue', text='Mejores Puntajes', width=19, fg='white', font=fuente_botones, command=puntajes)
boton_puntajes.place(x=85, y=250)

boton_about = tk.Button(ventana_principal, bg='midnight blue', text='A cerca de', width=19, fg='white', font=fuente_botones, command=about)
boton_about.place(x=85, y=330)

boton_conf = tk.Button(ventana_principal, bg='midnight blue', text='Configuracion', width=19, fg='white', font=fuente_botones, command=configuracion)
boton_conf.place(x=85, y=410)

boton_ayuda = tk.Button(ventana_principal, bg='midnight blue', text='Ayuda', width=19, fg='white', font=fuente_botones, command=ayuda)
boton_ayuda.place(x=85, y=490)

#Cargar el logo
logo = Image.open('Imagenes/_titulo_.png')
logo_tk = ImageTk.PhotoImage(logo)

label_logo = tk.Label(ventana_principal, image=logo_tk, bg='midnight blue', height=150)
label_logo.place(x=155, y=5)

ventana_principal.mainloop()