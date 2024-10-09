import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import os

# Variable para almacenar el proceso activo
proceso_activo = None

# Función para ejecutar el primer script Python
def ejecutar_script1():
    global proceso_activo
    if proceso_activo is not None:
        print("Ya hay un proceso en ejecución")
        return
    script1_path = os.path.join(os.getcwd(), "examen.py")
    proceso_activo = subprocess.Popen(["python3", script1_path])

# Función para ejecutar el segundo script Python
def ejecutar_script2():
    global proceso_activo
    if proceso_activo is not None:
        print("Ya hay un proceso en ejecución")
        return
    script2_path = os.path.join(os.getcwd(), "uniogmailybot.py")
    proceso_activo = subprocess.Popen(["python3", script2_path])

# Función para cancelar la ejecución
def cancelar_ejecucion():
    global proceso_activo
    if proceso_activo is not None:
        proceso_activo.terminate()  # Terminar el proceso activo
        proceso_activo = None  # Reiniciar la variable
        print("Proceso cancelado.")
    ventana.destroy()  # Cerrar la ventana y detener el programa

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Entorno de control tipo shell")
ventana.geometry("300x200")  # Tamaño de la ventana

# Cargar la imagen de fondo desde la ruta
ruta_imagen = os.path.expanduser("~/labo1/miniproy/raspy/audi-cool-logos-3hqni7p0ztne1vqn.jpg")
imagen_fondo = Image.open(ruta_imagen)
imagen_fondo = imagen_fondo.resize((300, 200), Image.ANTIALIAS)  # Ajustar la imagen al tamaño de la ventana
imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo)

# Crear un label para la imagen de fondo
fondo_label = tk.Label(ventana, image=imagen_fondo_tk)
fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

# Crear los botones y asignarles las funciones
boton1 = tk.Button(ventana, text="TEST", command=ejecutar_script1, bg='gray', fg='white')
boton1.pack(pady=20)

boton2 = tk.Button(ventana, text="SMALL PROYECT", command=ejecutar_script2, bg='gray', fg='white')
boton2.pack(pady=20)

# Botón de cancelar
boton_cancelar = tk.Button(ventana, text="Cancelar", command=cancelar_ejecucion, bg='gray', fg='white')
boton_cancelar.pack(pady=20)

# Correr el loop principal de la ventana
ventana.mainloop()
