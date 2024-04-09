import io
import picamera
import cv2
import numpy as np
import serial  

# Inicialização da PiCamera
camera = picamera.PiCamera()

# Inicialização da comunicação UART
uart = serial.Serial('/dev/tty1', baudrate=115200, timeout=1)  

try:
    # Loop enquanto a câmera estiver aberta
    while True:
        # Captura da imagem pela PiCamera
        stream = io.BytesIO()
        camera.capture(stream, format='jpeg')
        stream.seek(0)
        
        # Leitura da imagem capturada
        data = np.frombuffer(stream.getvalue(), dtype=np.uint8)
        img = cv2.imdecode(data, 1)

        # Transformação da imagem para escala HSV
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Definição dos limites do filtro
        hmin, smin, vmin = 55, 0, 160
        hmax, smax, vmax = 179, 73, 255

        lower = np.array([hmin, smin, vmin])
        upper = np.array([hmax, smax, vmax])

        # Aplicação da máscara
        mask = cv2.inRange(img_hsv, lower, upper)

        # Encontrar contornos na imagem
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Calcular a maior área
        max_area = 0
        max_contour = None
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                max_contour = contour

        # Calcular o centroide do maior contorno
        if max_contour is not None:
            M = cv2.moments(max_contour)
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            cx, cy = 0, 0

        # Enviar dados por UART
        uart_data = f"Area: {max_area}, Centroide: ({cx}, {cy})\n"
        uart.write(uart_data.encode())

except KeyboardInterrupt:
    # Encerrar a câmera e a comunicação UART quando o programa for interrompido
    camera.close()
    uart.close()
