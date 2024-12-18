import tkinter as tk
import time
from tkinter import ttk
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from PIL import Image, ImageTk, ImageSequence  
import serial
import csv
from datetime import datetime
from tkinter import simpledialog, messagebox
import threading  

# Configuración del puerto serial
serial_port = 'COM6'  
baud_rate = 115200
ser = serial.Serial(serial_port, baud_rate)

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
    print(f"Cargando datos del archivo: {archivo}")
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

# Función para manejar la selección de un archivo CSV
def seleccionar_csv(listbox_csv):
    archivo_seleccionado = listbox_csv.get(tk.ACTIVE)  # Obtener el archivo seleccionado
    print(f"Archivo seleccionado: {archivo_seleccionado}")
    if archivo_seleccionado:
        graficar_csv_tiempo_real(archivo_seleccionado)
    else:
        print("No se seleccionó ningún archivo.")

# Función para generar el nombre del archivo CSV
def generate_filename(patient_name):
    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y_%H-%M")
    return f"{patient_name}_{date_time}.csv"

# Estado de la medición (para detenerla)
medicion_activa = False

# Función para iniciar la medición en un hilo separado
def iniciar_medicion():
    global medicion_activa
    if medicion_activa:
        messagebox.showinfo("Aviso", "La medición ya está en curso.")
        return
    
    # Solicitar el nombre del paciente
    patient_name = simpledialog.askstring("Nombre del Paciente", "Ingrese el nombre del paciente:")
    if not patient_name:
        messagebox.showwarning("Aviso", "Debe ingresar un nombre para iniciar la medición.")
        return

    filename = generate_filename(patient_name)

    pitch_data = []
    yaw_data = []
    roll_data = []

    # Iniciar medición en un hilo separado
    def medicion_thread():
        global medicion_activa
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Pitch", "Yaw", "Roll"])
            messagebox.showinfo("Iniciando", "Medición iniciada. Presione 'Detener Medición' para detener.")
            medicion_activa = True  # Marcar que la medición está en curso

            try:
                while medicion_activa:  # Continuar mientras la medición esté activa
                    if ser.in_waiting:
                        line = ser.readline().decode('utf-8').strip()
                        print(f"Línea recibida: {line}")

                        try:
                            if "Pitch" in line and "Yaw" in line and "Roll" in line:
                                parts = line.split()
                                pitch = float(parts[1].strip(","))
                                yaw = float(parts[3].strip(","))
                                roll = float(parts[5].strip(","))

                                pitch_data.append(pitch)
                                yaw_data.append(yaw)
                                roll_data.append(roll)
                                writer.writerow([pitch, yaw, roll])
                                file.flush()

                                print(f"Datos guardados: Pitch={pitch}, Yaw={yaw}, Roll={roll}")
                        except (ValueError, IndexError) as e:
                            print(f"Error procesando línea: {line} - {e}")
            except KeyboardInterrupt:
                print("Medición detenida por el usuario.")
            finally:
                ser.close()
                medicion_activa = False  # Marcar que la medición ha terminado
                print(f"Archivo '{filename}' guardado correctamente y puerto cerrado.")

    # Ejecutar el hilo de medición
    threading.Thread(target=medicion_thread, daemon=True).start()

# Función para detener la medición
def detener_medicion():
    global medicion_activa
    medicion_activa = False  # Detener la medición
    messagebox.showinfo("Medición detenida", "La medición ha sido detenida exitosamente.")

# Función para mostrar la medición de frecuencia respiratoria
def mostrar_medicion():
    for widget in panel_derecho.winfo_children():
        widget.destroy()
    etiqueta_medicion = tk.Label(panel_derecho, text="MEDICIÓN DE FRECUENCIA RESPIRATORIA", font=("Century Gothic", 19, "bold"), fg="#274C50", bg="#D6EAF8")

    etiqueta_medicion.pack(pady=20)

    # Botón para iniciar la medición
    boton_iniciar_medicion = tk.Button(panel_derecho, text="Iniciar Medición", command=iniciar_medicion, bd=3, bg="#427c8a", cursor="hand2", fg="white", font=("Arial", 12, "bold"), height=2, padx=10, pady=5, width=15)
    boton_iniciar_medicion.pack(pady=20)

    # Botón para detener la medición
    boton_detener_medicion = tk.Button(panel_derecho, text="Detener Medición", command=detener_medicion, bd=3, bg="#FF5733", cursor="hand2", fg="white", font=("Arial", 12, "bold"), height=2, padx=10, pady=5, width=15)
    boton_detener_medicion.pack(pady=20)

# Función para mostrar la información del usuario
def mostrar_usuario():
    for widget in panel_derecho.winfo_children():
        widget.destroy()
    etiqueta_usuario = tk.Label(panel_derecho, text="INFORMACIÓN DEL USUARIO", font=("Century Gothic", 19, "bold"), fg="#274C50", bg="#D6EAF8")
    etiqueta_usuario.pack(pady=20)

    # Aquí eliminamos las líneas que mostraban nombre y edad del usuario
    # Crear un listbox para seleccionar los archivos CSV
    listbox_csv = tk.Listbox(panel_derecho, height=15, width=50)
    listbox_csv.pack(pady=20)

    # Cargar archivos CSV al listbox
    archivos_csv = cargar_archivos_csv()
    for archivo in archivos_csv:
        listbox_csv.insert(tk.END, archivo)

    # Botón para seleccionar un archivo CSV
    boton_seleccionar = tk.Button(panel_derecho, text="Seleccionar Archivo", command=lambda: seleccionar_csv(listbox_csv))
    boton_seleccionar.pack(pady=10)

# Ventana principal
ventana_principal = tk.Tk()
ventana_principal.geometry('1000x600')
ventana_principal.title("Sensor BreathWave")

try:
    icono = ImageTk.PhotoImage(Image.open("logobreath.png"))
    ventana_principal.iconphoto(True, icono)
except FileNotFoundError:
    print("Icono logobreath.png no encontrado.")

# Pantalla inicial
pantalla_inicial = tk.Frame(ventana_principal, bg="#FFFFFF")
pantalla_inicial.pack(fill="both", expand=True)
textin = tk.Label(pantalla_inicial, text=f"\n\nSENSOR BREATHWAVE\nBienvenido",
                  font=("Century Gothic", 30, "bold"), bg="#FFFFFF", fg="#274C50")
textin.pack()

try:
    gif = Image.open("verdebendito.gif") 
    gif_frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]
    gif_indice = [0]
    etiqueta_gif = tk.Label(pantalla_inicial, bg="#FFFFFF")
    etiqueta_gif.pack(fill="both", expand=True)
    reproducir_gif()  # Iniciar reproducción del GIF
except FileNotFoundError:
    print("GIF verdebendito.gif no encontrado.")

# Botón para cambiar a la vista de los paneles
boton_iniciar = tk.Button(pantalla_inicial, text="Iniciar", command=mostrar_paneles,
                          font=("Arial", 14, "bold"), bg="#427c8a", fg="white", padx=20, pady=10, cursor="hand2")
boton_iniciar.pack(pady=20)

# Paneles izquierdo y derecho
panel_izquierdo = tk.Frame(ventana_principal, width=150, bg="#8CC9D2")
panel_derecho = tk.Frame(ventana_principal, bg="#D6EAF8")

imagen_panel_izquierdo = Image.open("logobreath.png")  
imagen_panel_izquierdo = imagen_panel_izquierdo.resize((160, 160), Image.Resampling.LANCZOS)
imagen_panel_izquierdo_tk = ImageTk.PhotoImage(imagen_panel_izquierdo)
etiqueta_imagen_izquierda = tk.Label(panel_izquierdo, image=imagen_panel_izquierdo_tk, bg="#8CC9D2")
etiqueta_imagen_izquierda.image = imagen_panel_izquierdo_tk
etiqueta_imagen_izquierda.place(x=0, y=0)
etiqueta_imagen_izquierda.pack()

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

# Botones en el panel izquierdo
boton1 = tk.Button(panel_izquierdo, text="Usuario", image=user ,compound="left",command=mostrar_usuario, bd=3, bg="#427c8a", cursor="hand2", fg="#c6d8dc", font=("Arial", 12, "bold"), height=35, padx=10, pady=5, width=100)
boton1.pack(padx=20, pady=20)

boton2 = tk.Button(panel_izquierdo, text="Medición", image=med, compound="left",command=mostrar_medicion, bd=3, bg="#427c8a", cursor="hand2", fg="#c6d8dc", font=("Arial", 12, "bold"), height=35, padx=10, pady=5, width=100)
boton2.pack(padx=20, pady=20)

boton3 = tk.Button(panel_izquierdo, text="Cerrar", image=close, compound="left",command=ventana_principal.destroy, bd=3, bg="#427c8a", cursor="hand2", fg="#c6d8dc", font=("Arial", 12, "bold"), height=35, padx=10, pady=5, width=100)
boton3.pack(padx=20, pady=20)

ventana_principal.mainloop()
