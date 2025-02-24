import time
import requests
from pynput import keyboard
import speech_recognition as sr

API_URL = "http://192.168.15.5:8000/process_audio"
recognizer = sr.Recognizer()
recording = False
running = True  # Sinal de execução global
audio_data = None

def capture_audio():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("🎤 Escutando... (Segure a barra de espaço)")
        try:
            audio_data = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            return audio_data
        except sr.WaitTimeoutError:
            print("⏳ Tempo limite sem áudio.")
            return None

def recognize_speech(audio_data):
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

def send_to_server(transcription):
    try:
        response = requests.post(
            API_URL, 
            json={
                "transcription": transcription
            }
        )
        if response.status_code == 200:
            print("✅ Resposta do servidor:", response.json())
        else:
            print("❌ Erro ao enviar para o servidor:", response.text)
    except requests.RequestException as e:
        print("🚨 Erro de conexão com o servidor:", e)

def on_press(key):
    global audio_data, recording
    if key == keyboard.Key.space and not recording:
        recording = True
        audio_data = capture_audio()

def on_release(key):
    global audio_data, recording
    if key == keyboard.Key.space and recording:
        recording = False

        if audio_data:
            transcription = recognize_speech(audio_data)
            if transcription and transcription != "":
                send_to_server(transcription)

        print("🛑 Parando gravação...")
        print("\nPressione a barra de espaço para falar...")

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
        print("✅ Programa encerrado com sucesso.")

if __name__ == "__main__":
    main()
