import speech_recognition as sr

# Inicializa o reconhecedor de voz
recognizer = sr.Recognizer()

# Captura o áudio do microfone
with sr.Microphone() as source:
    print("Fale algo...")
    recognizer.adjust_for_ambient_noise(source)  # Ajusta para ruídos do ambiente
    audio = recognizer.listen(source, phrase_time_limit=5)

# Converte áudio para texto
try:
    text = recognizer.recognize_google(audio, language="pt-BR")  # Define o idioma (Português-BR)
    print(f"Você disse: {text}")
except sr.UnknownValueError:
    print("Não entendi o que você disse.")
except sr.RequestError:
    print("Erro ao conectar-se ao serviço de reconhecimento de voz.")
