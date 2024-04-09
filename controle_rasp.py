import serial
import subprocess
import threading

# Função para executar o código da Missão 1
def executar_missao1():

    subprocess.run(["python3", "missao1.py"])

# Função para executar o código da Missão 2
def executar_missao2():
    
    subprocess.run(["python3", "missao2.py"])

# Configurar a porta serial (UART)
porta_serial = serial.Serial("/dev/tty1", baudrate=115200, timeout=1)

# Função para receber comandos da porta serial e executar a missão correspondente
def receber_comandos():
    while True:
        # Ler o comando enviado pelo STM32 via UART
        comando = porta_serial.readline().strip().decode("utf-8")
        
        # Interpretar o comando recebido
        if comando == "0":
            # Iniciar a execução da Missão 1 em uma nova thread
            threading.Thread(target=executar_missao1).start()
        elif comando == "1":
            # Iniciar a execução da Missão 2 em uma nova thread
            threading.Thread(target=executar_missao2).start()
        elif comando == "2":
            # Parar a execução do código
            print("Recebido comando para parar a execução")
            break

# Loop principal
while True:
    # Chamar a função para receber comandos
    receber_comandos()

# Fechar a porta serial (provavelmente nunca chegará aqui se o loop for contínuo)
porta_serial.close()
