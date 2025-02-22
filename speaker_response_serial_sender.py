import os
import time
import json
import serial
import threading
from pynput import keyboard
import speech_recognition as sr
from assistant_openai import generate_command

recognizer = sr.Recognizer()
recording = False
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
    global recording, audio_data
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

def on_press(key):
    global recording
    if key == keyboard.Key.space and not recording:
        recording = True
        capture_audio()

def on_release(key):
    global recording
    if key == keyboard.Key.space and recording:
        recording = False
        command = json.loads(generate_command(recognize_speech()))
        print(command)

        # Comandos do assistente
        text_response = command["text_response"]
        eyes_expression = command["eyes_expression"]
        robot_commands = command["robot_commands"]

        # Falar resposta
        speech(text_response)
        # send_command(command)

        print("🛑 Parando gravação...")
        print("Pressione a barra de espaço para falar...")

def main():
    global running
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    
    print("Pressione a barra de espaço para falar...")

    try:
        while running:
            time.sleep(0.1)  # Pequena pausa para evitar uso excessivo da CPU
    except KeyboardInterrupt:
        print("\n🚀 Encerrando programa...")
        running = False
        listener.stop()
        # arduino.close()
        print("✅ Programa encerrado com sucesso.")

if __name__ == "__main__":
    main()
