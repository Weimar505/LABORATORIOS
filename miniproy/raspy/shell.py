import tkinter as tk
from PIL import Image, ImageTk  # Necesitarás instalar Pillow: pip install pillow
import subprocess
import os

# Función para ejecutar el primer script Python
def ejecutar_script1():
    script1_path = os.path.join(os.getcwd(), "examen.py")  # Ruta completa al script1.py
    subprocess.run(["python3", script1_path])  # Ejecutar script1.py

# Función para ejecutar el segundo script Python
def ejecutar_script2():
    script2_path = os.path.join(os.getcwd(), "uniogmailybot.py")  # Ruta completa al script2.py
    subprocess.run(["python3", script2_path])  # Ejecutar script2.py

# Función para cancelar la ejecución
def cancelar_ejecucion():
    # Puedes realizar otras limpiezas aquí si es necesario
    print("Cancelando ejecución...")
    ventana.destroy()  # Cerrar la ventana y detener el programa

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Entorno de control tipo shell")
ventana.geometry("800x700")  # Tamaño de la ventana

# Cargar la imagen de fondo
imagen_fondo = Image.open("/home/kaku/labo1/miniproy/raspy/audi-cool-logos-3hqni7p0ztne1vqn.jpg")  # Especifica la ruta de la imagen
imagen_fondo = imagen_fondo.resize((800, 700), Image.LANCZOS)  # Redimensionar la imagen
imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo)

# Crear un label para la imagen de fondo
fondo_label = tk.Label(ventana, image=imagen_fondo_tk)
fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

# Crear los botones y asignarles las funciones
boton1 = tk.Button(ventana, text="TEST", command=ejecutar_script1)
boton1.pack(pady=20)  # Empaquetar con separación vertical

boton2 = tk.Button(ventana, text="SMALL PROYECT", command=ejecutar_script2)
boton2.pack(pady=20)  # Empaquetar con separación vertical

# Botón de cancelar
boton_cancelar = tk.Button(ventana, text="Cancelar", command=cancelar_ejecucion)
boton_cancelar.pack(pady=20)  # Empaquetar con separación vertical

# Correr el loop principal de la ventana
ventana.mainloop()
