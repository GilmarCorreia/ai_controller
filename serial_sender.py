import serial
import time

from command_generator import generate_command
#from command_generator_diana import generate_command

# Configurar porta serial (substitua 'COM3' pelo seu porto no Windows ou '/dev/ttyUSB0' no Linux)
#arduino = serial.Serial('COM3', 115200, timeout=1)
#arduino = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
time.sleep(2)

def send_command(command):
    commands = command.split("\n")
    print(commands)
    for command in commands:
        #print(f"{command}\n".encode())
        pass
        #arduino.write(f"{command}\n".encode())  # Envia o comando para o Arduino

def main():
    try:
        print("Pressione Ctrl+C para sair.")
        while True:
            input_text = input("Digite uma ação: ")
            command = generate_command(input_text)
            send_command(command)
            time.sleep(0.5)  # Evita uso excessivo da CPU
    except KeyboardInterrupt:
        print("\nPrograma encerrado pelo usuário.")

    #arduino.close()

if __name__ == "__main__":
    main()
