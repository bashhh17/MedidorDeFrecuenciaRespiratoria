import tkinter as tk
from tkinter import ttk
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk, ImageSequence  # Para manejar GIFs animados
import pandas as pd

# Función para mostrar la ventana principal con los paneles
def mostrar_paneles():
    pantalla_inicial.pack_forget()  # Oculta la pantalla inicial
    ventana_principal.config(background='#FCFCFC')  # Cambiar el fondo de la ventana
    panel_izquierdo.pack(side="left", fill="y")  # Muestra el panel izquierdo
    panel_derecho.pack(side="right", expand=True, fill="both")  # Muestra el panel derecho

# Función para reproducir el GIF
def reproducir_gif():
    frame = gif_frames[gif_indice[0]]  # Obtener el frame actual   
    gif_indice[0] = (gif_indice[0] + 1) % len(gif_frames)  # Actualizar el índice del frame
    etiqueta_gif.config(image=frame)  # Actualizar la imagen en el Label
    pantalla_inicial.after(20, reproducir_gif)  # Llamar de nuevo en 50 ms para mayor velocidad

# Función para cargar los archivos CSV de la carpeta actual
def cargar_archivos_csv():
    archivos_csv = [f for f in os.listdir() if f.endswith('.csv')]  # Buscar archivos CSV
    return archivos_csv

# Función para graficar datos del CSV progresivamente en tiempo real
def graficar_csv_tiempo_real(archivo):

    # Cargar el archivo CSV usando pandas
    df = pd.read_csv(archivo)
        
    # Crear la columna de 'Tiempo' si no existe
    if 'Tiempo' not in df.columns:
        df['Tiempo'] = [i * 0.1 for i in range(len(df))]
        
    # Usar la primera columna como 'Valor'
    valor = df.iloc[:, 0]
    tiempo = df['Tiempo']

    # Limpiar gráficos previos
    for widget in panel_derecho.winfo_children():
        if isinstance(widget, FigureCanvasTkAgg):
            widget.get_tk_widget().destroy()

    # Crear una nueva figura y eje
    fig, ax = plt.subplots()
    ax.set_title('Gráfica en Tiempo Real')
    ax.set_xlabel('Tiempo (segundos)')
    ax.set_ylabel('Valor')

    # Insertar la figura en la interfaz
    canvas = FigureCanvasTkAgg(fig, master=panel_derecho)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Listas para mantener los datos graficados hasta el momento
    x_data = []
    y_data = []

    # Función para actualizar la gráfica progresivamente
    def actualizar_grafica(indice):
        if indice < len(tiempo):
            x_data.append(tiempo[indice])
            y_data.append(valor[indice])
            ax.plot(x_data, y_data, color='blue')  # Actualizar la línea
            canvas.draw()  # Redibujar el canvas
            panel_derecho.after(100, actualizar_grafica, indice + 1)  # Llamar a la función para el siguiente índice

    # Iniciar la actualización progresiva
    actualizar_grafica(0)

# Modificar la función seleccionar_csv para usar la gráfica en tiempo real
def seleccionar_csv():
    archivo_seleccionado = listbox_csv.get(tk.ACTIVE)  # Obtener el archivo seleccionado
    print(f"Archivo seleccionado: {archivo_seleccionado}")
    graficar_csv_tiempo_real(archivo_seleccionado)  # Usar la gráfica progresiva

# Ventana principal
ventana_principal = tk.Tk()
ventana_principal.geometry('1000x600')
ventana_principal.title("Sensor BreathWave")
icono = ImageTk.PhotoImage(Image.open("Logodeadebis.png"))
ventana_principal.iconphoto(True, icono)

# Pantalla inicial
pantalla_inicial = tk.Frame(ventana_principal, bg="#FFFFFF")
pantalla_inicial.pack(fill="both", expand=True)
textin = tk.Label(pantalla_inicial, text=f"\n\nSENSOR BREATHWAVE\nBienvenido",
                  font=("Century Gothic", 30, "bold"), bg="#FFFFFF", fg="#274C50")
textin.pack()

# Cargar el GIF animado
gif = Image.open("verdebendito.gif") 
gif_frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]  # Extraer frames
gif_indice = [0]  # Índice para rastrear el frame actual

# Etiqueta para mostrar el GIF
etiqueta_gif = tk.Label(pantalla_inicial, bg="#FFFFFF")
etiqueta_gif.pack(fill="both", expand=True)
reproducir_gif()  # Iniciar reproducción del GIF

# Botón para cambiar a la vista de los paneles
boton_iniciar = tk.Button(pantalla_inicial, text="Iniciar", command=mostrar_paneles,
                          font=("Arial", 14, "bold"), bg="#427c8a", fg="white", padx=20, pady=10, cursor="hand2")
boton_iniciar.pack(pady=20)

# Paneles izquierdo y derecho
panel_izquierdo = tk.Frame(ventana_principal, width=150, bg="#8CC9D2")
panel_derecho = tk.Frame(ventana_principal, bg="#D6EAF8")
panel_derecho1 = tk.Frame(panel_derecho, bg="#D6EAF8")

#Imagenes botones usuarios y medición:
#Usuarios
file="usuario.png"
usuario1= Image.open(file)
usuario1=usuario1.resize((30,30), Image.Resampling.LANCZOS)
user=ImageTk.PhotoImage(usuario1)
#Medición
file2="medicion.png"
medicion1= Image.open(file2)
medicion1=medicion1.resize((30,30), Image.Resampling.LANCZOS)
med=ImageTk.PhotoImage(medicion1)
#Cerrar
file3="cerrar.png"
cerrar= Image.open(file3)
cerrar=cerrar.resize((30,30), Image.Resampling.LANCZOS)
close=ImageTk.PhotoImage(cerrar)
# Funciones para actualizar el contenido del panel derecho
def mostrar_usuario():
    global listbox_csv  # Hacer que listbox_csv sea accesible globalmente
    for widget in panel_derecho.winfo_children():
        widget.destroy()
    etiqueta_usuario = tk.Label(panel_derecho, text="INFORMACIÓN DE USUARIO", font=("Century Gothic", 19, "bold"), fg="#274C50", bg="#D6EAF8")
    etiqueta_usuario.pack(pady=20)
    
    # Mostrar archivos CSV en un Listbox con Scrollbar
    archivos_csv = cargar_archivos_csv()  # Obtener los archivos CSV
    scrollbar = tk.Scrollbar(panel_derecho)
    scrollbar.pack(side=tk.RIGHT, fill="y")
        
    listbox_csv = tk.Listbox(panel_derecho, yscrollcommand=scrollbar.set, height=15, width=80)
    for archivo in archivos_csv:
        listbox_csv.insert(tk.END, archivo)  # Insertar archivos CSV en el Listbox
    
    listbox_csv.pack(side=tk.TOP, fill=tk.Y)
    scrollbar.config(command=listbox_csv.yview)
    
    # Botón para seleccionar el archivo CSV
    boton_seleccionar = tk.Button(panel_derecho, text="Seleccionar usuario y gráficar datos", command=seleccionar_csv)
    boton_seleccionar.pack(pady=10)

def mostrar_medicion():
    for widget in panel_derecho.winfo_children():
        widget.destroy()
    etiqueta_medicion = tk.Label(panel_derecho, text="MEDICIÓN DE FRECUENCIA RESPIRATORIA", font=("Century Gothic", 19, "bold"), fg="#274C50", bg="#D6EAF8")
    etiqueta_medicion.pack(pady=20)

def mostrar_grafica_medicion(): 
    # Generar la gráfica 
    fig, ax = plt.subplots() 
    ax.plot([1, 2, 3, 4], [1, 2, 0, 0.5]) 
    # Mostrar la gráfica en la interfaz Tkinter 
    canvas = FigureCanvasTkAgg(fig, master=panel_derecho) 
    canvas.draw() 
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Cargar imagen en el panel izquierdo
imagen_panel_izquierdo = Image.open("logobreath.png")  
imagen_panel_izquierdo = imagen_panel_izquierdo.resize((160, 160), Image.Resampling.LANCZOS)
imagen_panel_izquierdo_tk = ImageTk.PhotoImage(imagen_panel_izquierdo)
etiqueta_imagen_izquierda = tk.Label(panel_izquierdo, image=imagen_panel_izquierdo_tk, bg="#8CC9D2")
etiqueta_imagen_izquierda.image = imagen_panel_izquierdo_tk
etiqueta_imagen_izquierda.place(x=0, y=0)
etiqueta_imagen_izquierda.pack()


# Botones en el panel izquierdo
boton1 = tk.Button(panel_izquierdo, text="Usuario", image=user, compound="left", command=mostrar_usuario,
                   bd=3, bg="#427c8a", cursor="hand2", fg="#c6d8dc", font=("Arial", 12, "bold"),
                   height=35, padx=10, pady=5, width=100)
boton1.pack(padx=20, pady=20)

boton2 = tk.Button(panel_izquierdo, text="Medición",image=med, compound="left", command=mostrar_medicion,
                   bd=3, bg="#427c8a", cursor="hand2", fg="#c6d8dc", font=("Arial", 12, "bold"),
                   height=35, padx=10, pady=5, width=100)
boton2.pack(padx=20, pady=20)
boton3=tk.Button(panel_izquierdo, text="Cerrar",image=close, compound="left", command=ventana_principal.destroy,
                   bd=3, bg="#427c8a", cursor="hand2", fg="#c6d8dc", font=("Arial", 12, "bold"),
                   height=35, padx=10, pady=5, width=100)
boton3.pack(padx=20, pady=20)
ventana_principal.mainloop()
