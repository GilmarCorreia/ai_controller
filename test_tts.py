import pyttsx3

def speech(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    print(voices)
    # Tentar escolher uma voz feminina robótica
    for voice in voices:
        if "female" in voice.name.lower():  # Pode mudar para "male" se quiser
            engine.setProperty('voice', voice.id)
            break
    
    engine.setProperty('rate', 180)  # Velocidade da fala (padrão é 200)
    engine.setProperty('pitch', 150)  # Pode ser ajustado conforme necessário
    
    engine.say(text)
    engine.runAndWait()


speech("  hahaha")