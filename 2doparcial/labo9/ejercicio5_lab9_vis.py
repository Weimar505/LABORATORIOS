import cv2
import serial
import threading
from abc import ABC, abstractmethod

class CapturaVideoAbs(ABC): # Definimos la clase abstracta
    @abstractmethod
    def mostrar_camara(self):
        pass

    @abstractmethod
    def detener_mostrar(self):
        pass

    @abstractmethod
    def visualizacion_camara(self):
        pass


class CapturaVideo(CapturaVideoAbs): # Clase
    def __init__(self, camara, puerto_serial) -> None: # Constructor
        self.camara = camara # Inicializar cámara
        self.mostrando = False # Bandera
        self.sustractor_fondo = cv2.createBackgroundSubtractorKNN() # Sustractor de fondo KNN
        self.serial = puerto_serial  # Comunicación UART

        # Iniciar un hilo para leer e imprimir datos recibidos por UART
        self.hilo_lectura_serial = threading.Thread(target=self.leer_datos_serial, daemon=True)
        self.hilo_lectura_serial.start()

        # Obtener dimensiones de la cámara para dividir en cuadrantes
        ret, cuadro = self.camara.read()
        if ret:
            self.alto, self.ancho = cuadro.shape[:2]
            # Definir las posiciones de los cuadrantes
            self.q_izquierda = self.ancho // 3
            self.q_derecha = 2 * self.ancho // 3
            self.centro_x, self.centro_y = self.ancho // 2, self.alto // 2
        else:
            self.alto = self.ancho = self.centro_x = self.centro_y = 0

    def leer_datos_serial(self):
        """Lee datos del puerto serial y los imprime en la consola."""
        while True:
            if self.serial.in_waiting > 0:  # Si hay datos disponibles en el puerto serial
                datos = self.serial.readline().decode('utf-8').strip()
                print(f"Datos recibidos por UART: {datos}")

    def mostrar_camara(self): # Método para iniciar la visualización de la cámara
        self.mostrando = True  # Activar la bandera de visualización
        self.visualizacion_camara()  # Llamar al método de visualización

    def detener_mostrar(self): # Método para detener la visualización de la cámara
        self.mostrando = False  # Desactivar la bandera de visualización

    def mover_direccion_objeto(self, centro_objeto_x):  # Método para mover en la dirección del objeto
        if centro_objeto_x < self.q_izquierda:  # Objeto en el cuadrante izquierdo
            self.serial.write(b'L')  # Comando para girar a la izquierda
            print("Objeto en cuadrante izquierdo, moviendo a la izquierda")
        elif centro_objeto_x > self.q_derecha:  # Objeto en el cuadrante derecho
            self.serial.write(b'R')  # Comando para girar a la derecha
            print("Objeto en cuadrante derecho, moviendo a la derecha")
        else:
            print("Objeto en el cuadrante central, no se envía comando de movimiento")

    def visualizacion_camara(self): # Método principal para la visualización y procesamiento de la cámara
        while self.mostrando:
            verificado, cuadro = self.camara.read()
            if not verificado:
                print("No se pudo capturar el cuadro. Verifica la cámara.")
                self.detener_mostrar()
                break

            # Aplicar sustracción de fondo para generar la máscara
            mascara_fg = self.sustractor_fondo.apply(cuadro)

            # Crear una versión en color de la máscara donde el objeto esté a color y el fondo en negro
            objeto_en_color = cv2.bitwise_and(cuadro, cuadro, mask=mascara_fg)

            # Encontrar contornos en la máscara
            contornos, _ = cv2.findContours(mascara_fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            objeto_detectado = False
            for contorno in contornos:
                if cv2.contourArea(contorno) < 400: # Ignorar contornos pequeños (ruido)
                    continue

                # Obtener el rectángulo delimitador del contorno
                x, y, w, h = cv2.boundingRect(contorno)
                
                # Calcular el centro del objeto
                centro_objeto_x = x + w // 2
                centro_objeto_y = y + h // 2

                # Verificar si el objeto está en el cuadrante central
                objeto_detectado = True
                
                # Dibujar un rectángulo alrededor del objeto detectado
                cv2.rectangle(objeto_en_color, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if objeto_detectado:
                cv2.putText(objeto_en_color, "Objeto Detectado", (self.ancho - 200, self.alto - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                self.mover_direccion_objeto(centro_objeto_x)  # Mover en dirección al objeto

            # Mostrar solo el objeto detectado en color y el fondo en negro
            cv2.imshow('Objeto Detectado en Color', objeto_en_color)

            tecla = cv2.waitKey(1)
            if tecla != -1:
                self.detener_mostrar()


# Configurar la comunicación serial con el puerto correcto
puerto_serial = serial.Serial('/dev/ttyACM0', 9600)  # Ajusta el puerto según sea necesario

camara = cv2.VideoCapture(0)  # Iniciar la cámara
if not camara.isOpened():
    print("Error: No se pudo abrir la cámara.")
else:
    objeto_camara = CapturaVideo(camara, puerto_serial)  # Crear objeto CapturaVideo
    objeto_camara.mostrar_camara()  # Comenzamos la visualización

camara.release()  # Liberar la cámara
cv2.destroyAllWindows()  # Cerrar ventanas de OpenCV al finalizar
puerto_serial.close()  # Cerrar la conexión serial al finalizar
