import cv2
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
    def __init__(self, camara) -> None: # Constructor
        
        self.camara = camara # Inicializar cámara
        self.mostrando = False # Bandera 
        self.sustractor_fondo = cv2.createBackgroundSubtractorKNN() # Sustractor de fondo KNN

        
        ret, cuadro = self.camara.read() # Obtener dimensiones de la cámara para calcular el centro del cuadro
        if ret:
            self.alto, self.ancho = cuadro.shape[:2]
            self.centro_x, self.centro_y = self.ancho // 2, self.alto // 2
        else:

            self.alto = self.ancho = self.centro_x = self.centro_y = 0 # Si no se puede leer el cuadro, establecer dimensiones en 0

    
    def mostrar_camara(self): # Método para iniciar la visualización de la cámara
        self.mostrando = True  # Activar la bandera de visualización
        self.visualizacion_camara()  # Llamar al método de visualización

    
    def detener_mostrar(self): # Método para detener la visualización de la cámara
        self.mostrando = False  # Desactivar la bandera de visualización

    
    def visualizacion_camara(self): # Método principal para la visualización y procesamiento de la cámara
        while self.mostrando:
            verificado, cuadro = self.camara.read()
            if not verificado:
 
                print("No se pudo capturar el cuadro. Verifica la cámara.") # Si no se puede leer el cuadro, mostrar mensaje de error y detener visualización
                self.detener_mostrar()
                break
            
            # Aplicar sustracción de fondo para generar la máscara
            mascara_fg = self.sustractor_fondo.apply(cuadro)

            # Crear una versión en color de la máscara donde el objeto esté a color y el fondo en negro
            objeto_en_color = cv2.bitwise_and(cuadro, cuadro, mask=mascara_fg)

            # Encontrar contornos en la máscara
            contornos, _ = cv2.findContours(mascara_fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            objeto_detectado = False  # Inicializar una bandera para verificar si se detecta un objeto en el centro
            for contorno in contornos:
                
                if cv2.contourArea(contorno) < 400: # Ignorar contornos pequeños (ruido)
                    continue

                # Obtener el rectángulo delimitador del contorno
                x, y, w, h = cv2.boundingRect(contorno)
                
                # Calcular el centro del objeto
                centro_objeto_x = x + w // 2
                centro_objeto_y = y + h // 2

                # Verificar si el centro del objeto pasa por el centro de la pantalla
                if (self.centro_x - self.ancho * 0.1 < centro_objeto_x < self.centro_x + self.ancho * 0.1 and
                    self.centro_y - self.alto * 0.1 < centro_objeto_y < self.centro_y + self.alto * 0.1):
                    objeto_detectado = True  # Activar la detección si el objeto está en el centro
                
                # Dibujar un rectángulo alrededor del objeto detectado
                cv2.rectangle(objeto_en_color, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if objeto_detectado: # Si detectamos un objeto muestra "Objeto Detectado"
                cv2.putText(objeto_en_color, "Objeto Detectado", (self.ancho - 200, self.alto - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            # Mostrar solo el objeto detectado en color y el fondo en negro
            cv2.imshow('Objeto Detectado en Color', objeto_en_color)
            cv2.imshow('Sustraccion de Fondo KNN', mascara_fg)

            tecla = cv2.waitKey(1)
            if tecla != -1:  # Cualquier tecla fue presionada
                self.detener_mostrar()


camara = cv2.VideoCapture(0)   # Iniciar la cámara
if not camara.isOpened():
    print("Error: No se pudo abrir la cámara.")
else:
    objeto_camara = CapturaVideo(camara) # Crear objeto CapturaVideo
    objeto_camara.mostrar_camara() # Comenzamos la visualización


camara.release() # Liberar la cámara 
cv2.destroyAllWindows() # Cerrar ventanas de OpenCV al finalizar

