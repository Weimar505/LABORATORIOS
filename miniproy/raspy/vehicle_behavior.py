import tkinter as tk
import subprocess
import os
import sys  # Importa sys para salir del programa

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
ventana.geometry("300x200")  # Tamaño de la ventana

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