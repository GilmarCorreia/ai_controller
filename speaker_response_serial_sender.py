import os
import time
import json
import serial
import threading
import keyboard
import speech_recognition as sr
from assistant_openai import generate_command

recognizer = sr.Recognizer()
audio_data = None
running = True  # Sinal de execução global

# Configurar porta serial (comente se não usar Arduino)
# arduino = serial.Serial('COM3', 115200, timeout=1)  # Para Windows
# arduino = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)  # Para Linux
time.sleep(2)

def send_command(command):
    commands = command.split("\n")
    print(commands)
    for command in commands:
        pass
        # arduino.write(f"{command}\n".encode())

def capture_audio():
    global audio_data
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("🎤 Escutando... (Segure a barra de espaço)")
        try:
            audio_data = recognizer.listen(source, timeout=10, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("⏳ Tempo limite sem áudio.")

def recognize_speech():
    global audio_data
    if audio_data:
        try:
            text = recognizer.recognize_google(audio_data, language="pt-BR")
            print(f"📝 Você disse: {text}")
            return text
        except sr.UnknownValueError:
            print("🤖 Não entendi o que você disse.")
        except sr.RequestError:
            print("❌ Erro ao acessar o serviço de reconhecimento.")
    return ""

def speech(texto):
    os.system(f'espeak -v pt+f3 -p 150 -s 160 "{texto}"')

def listen_for_space():
    """Thread para capturar áudio enquanto a barra de espaço estiver pressionada."""
    global running
    while running:
        print("Pressione a barra de espaço para falar...")
        keyboard.wait("space")  # Aguarda pressionamento da tecla
        print("🎤 Gravando... Segure a barra de espaço.")

        capture_audio()  # Captura o áudio enquanto pressionado

        print("🛑 Parando gravação...")
        command = json.loads(generate_command(recognize_speech()))
        print(command)

        # Comandos do assistente
        text_response = command["text_response"]
        eyes_expression = command["eyes_expression"]
        robot_commands = command["robot_commands"]

        # Falar resposta
        speech(text_response)
        # send_command(command)

def main():
    global running
    listener_thread = threading.Thread(target=listen_for_space, daemon=True)
    listener_thread.start()

    try:
        while running:
            time.sleep(0.1)  # Pequena pausa para evitar uso excessivo da CPU
    except KeyboardInterrupt:
        print("\n🚀 Encerrando programa...")
        running = False
        print("✅ Programa encerrado com sucesso.")

if __name__ == "__main__":
    main()
