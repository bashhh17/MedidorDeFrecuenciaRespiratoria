import serial
import csv
import os
import keyboard  # Para detectar la pulsación de teclas
from datetime import datetime  # Para obtener fecha y hora

# Configuración del puerto serial
serial_port = 'COM6'  # Cambia esto al puerto correcto
baud_rate = 115200
ser = serial.Serial(serial_port, baud_rate)

# Función para generar el nombre del archivo CSV
def generate_filename():
    print("Nombre del paciente")
    base_name = input().strip()  # Captura el nombre del paciente

    # Obtiene la fecha y hora actuales
    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y_%H-%M")  # Formato: Día-Mes-Año_Hora-Minutos

    # Genera el nombre del archivo con la fecha y hora
    filename = f"{base_name}_{date_time}.csv"
    return filename

# Función principal para capturar y guardar datos
def capture_and_save_data():
    # Genera el nombre del archivo y abre el archivo CSV en modo de escritura
    filename = generate_filename()

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        # Escribe encabezados para los datos procesados
        writer.writerow(["Pitch", "Yaw", "Roll"])

        print("Leyendo datos del sensor. Presiona 'Escape' para detener la ejecución.")

        try:
            while True:
                # Si la tecla Escape es presionada, termina el programa
                if keyboard.is_pressed("esc"):
                    print("\nTecla Escape detectada. Deteniendo la lectura.")
                    break

                # Si hay datos disponibles en el puerto serial
                if ser.in_waiting:
                    line = ser.readline().decode('utf-8').strip()
                    print(f"Línea recibida: {line}")  # Muestra los datos en la terminal

                    try:
                        # Procesa los datos en el formato "Pitch valor    Yaw valor    Roll valor"
                        if "Pitch" in line and "Yaw" in line and "Roll" in line:
                            parts = line.split()  # Divide por espacios
                            pitch = float(parts[1].strip(","))
                            yaw = float(parts[3].strip(","))
                            roll = float(parts[5].strip(","))

                            # Guarda únicamente los datos procesados en el archivo CSV
                            writer.writerow([pitch, yaw, roll])
                            file.flush()  # Asegura que los datos se escriban inmediatamente

                            print(f"Datos guardados: Pitch={pitch}, Yaw={yaw}, Roll={roll}")
                        else:
                            print(f"Formato de línea no reconocido o incompleto: {line}")
                    except (ValueError, IndexError) as e:
                        print(f"Error procesando línea: {line} - {e}")

        except Exception as e:
            print(f"Error inesperado: {e}")

        finally:
            # Cierra el puerto serial al finalizar
            ser.close()
            print(f"Archivo '{filename}' guardado correctamente y puerto cerrado.")

# Llamada a la función principal
capture_and_save_data()
