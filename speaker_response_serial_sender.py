import time
import json
import serial
import pyttsx3
import keyboard
import speech_recognition as sr
from assistant_openai import generate_command

# Inicializa o reconhecedor de voz
recognizer = sr.Recognizer()

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

def capture_audio():
    # Captura o áudio do microfone
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)

        # Captura contínua enquanto a tecla estiver pressionada
        audio = None
        while keyboard.is_pressed("space"):
            try:
                print("Escutando...")
                audio = recognizer.listen(source, timeout=0.5, phrase_time_limit=5)
            except sr.WaitTimeoutError:
                pass  # Se não houver áudio, continua esperando

        # Se capturou áudio, faz o reconhecimento
        if audio:
            try:
                text = recognizer.recognize_google(audio, language="pt-BR")
                print("Você disse:", text)
            except sr.UnknownValueError:
                print("Não entendi o que você disse.")
            except sr.RequestError:
                print("Erro ao acessar o serviço de reconhecimento.")
    
    return text

def speech(texto):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # Tentar escolher uma voz feminina robótica
    for voice in voices:
        if "female" in voice.name.lower():  # Pode mudar para "male" se quiser
            engine.setProperty('voice', voice.id)
            break
    
    engine.setProperty('rate', 180)  # Velocidade da fala (padrão é 200)
    #engine.setProperty('pitch', 150)  # Pode ser ajustado conforme necessário
    
    engine.say(texto)
    engine.runAndWait()

def main():
    try:
        print("Pressione Ctrl+C para sair.")
        while True:

            print("Pressione 'espaço' para falar...")
            keyboard.wait("space")
            command = json.loads(generate_command(capture_audio()))

            print(command)

            # Get the command from the OpenAI Assistant
            text_response = command["text_response"]
            eyes_expression = command["eyes_expression"]
            robot_commands = command["robot_commands"]

            # Speak the response
            speech(text_response)

            #send_command(command)
            time.sleep(0.5)  # Evita uso excessivo da CPU
    except KeyboardInterrupt:
        print("\nPrograma encerrado pelo usuário.")

    #arduino.close()

if __name__ == "__main__":
    main()
