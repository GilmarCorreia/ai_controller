import serial
import time

#from command_generator import generate_command

# Configurar porta serial (substitua 'COM3' pelo seu porto no Windows ou '/dev/ttyUSB0' no Linux)
arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

def send_command(command):
    commands = command.split("\n")
    print(commands)

    for command in commands:
        print(f"{command}\n".encode())
        arduino.write(f"{command}\n".encode())  # Envia o comando para o Arduino

command = "MF5\nMF6"
#command = generate_command("move as a square, each size 7 seconds")
print(command)
send_command(command)

arduino.close()
