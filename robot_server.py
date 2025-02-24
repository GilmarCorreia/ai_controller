import os
import time
import json
import asyncio
import serial
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from assistant_openai import generate_command

# Configurar porta serial (se necessário)
arduino = serial.Serial('COM5', 9600, timeout=1)  # Para Windows
# arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Para Linux
time.sleep(2)

app = FastAPI()

class AudioTranscription(BaseModel):
    transcription: str

def send_command(commands):
    #commands = command.split("\n")
    print(commands)
    for command in commands:
        arduino.write(f"{command}\n".encode())

def speech(text):
    os.system(f'espeak -v pt+f3 -p 150 -s 160 "{text}"')

@app.post("/process_audio")
async def process_audio(data: AudioTranscription):
    try:
        # Gerar comando a partir da transcrição
        command = json.loads(generate_command(data.transcription))
        print(command)

        # Extrair informações do comando
        text_response = command["text_response"]
        eyes_expression = command.get("eyes_expression", "neutral")
        robot_commands = command.get("robot_commands", "")

        # Executar ações simultaneamente
        await asyncio.gather(
            asyncio.to_thread(speech, text_response),
            asyncio.to_thread(send_command, eyes_expression)
        )

        await asyncio.to_thread(send_command, robot_commands)

        return {"message": "Comando processado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
