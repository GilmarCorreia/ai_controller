import json
import requests

main_url = "https://dianaapi-543834107372.us-central1.run.app/"
key = "cba401af31b045de4b45cfb82df9ffe62ecc2b99ca9edbc2aef1738868e3745a"
name = "External-Dev"

# Get access token
url = f"{main_url}token?key={key}&accessName={name}"
response = requests.get(url)

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    dados = response.json()  # Converte a resposta para JSON (se aplicável)
    token = dados.get("token")
    # Configura o cabeçalho de autorização com o Bearer Token
    headers = {
        "Authorization": f"Bearer {token}"
    }
else:
    raise Exception(f"Erro na requisição: {response.status_code}")

# Get session
response = requests.get(f"{main_url}session", headers=headers)

if response.status_code == 200:
    dados = response.json()
    session = dados.get("session")
else:
    raise Exception(f"Erro na requisição: {response.status_code}")

def generate_command(action):
    # Construct the prompt for the LLM
    prompt = f"""
----- Instructions -----

Generate a sequence of commands to perform a robot action. Each command should be on a new line.
The available commands are:
   - 'ONx': Starts the engine at an analog speed 'x' (range: 100 to 255);
   - 'OFF': Stops the robot;
   - 'MFx': Moves the robot forward for 'x' milliseconds;
   - 'MBx': Moves the robot backwards for 'x' milliseconds;
   - 'BLx': Blinks an LED for 'x' milliseconds;
   - 'CCWx': Rotates the robot counterclockwise by an angle 'x' in degrees;
   - 'CWx': Rotates the robot clockwise by an angle 'x' in degrees.

Note: The sequence must start with 'ONx' and end with 'OFF', except when blinking the LED. Ensure that all values for 'x' (speed, time, and angle) are positive numbers.
Examples:

1
Action: move forward with max speed for 3 seconds
ON255
MF3000
OFF

2
Action: blink a LED for 3 seconds.
BL3000

3
Action: Start running
ON255

4
Action: Stop running
OFF

5
Action: Move backwards with 100% of speed for 5 seconds and when it stop blink a LED for 3 seconds.
ON255
MB5000
OFF
BL3000

6
Action: Rotate the robot counterclockwise by 90 degrees.
CCW90

7
Action: Rotate the robot clockwise by 180 degrees.
CW180

Our action is:
Action: {action}
"""
    # Get session
    data = {
        "text": prompt,
        "session": session
    }
    response = requests.post(f"{main_url}textIntent", headers=headers, json=data)

    if response.status_code == 200:
        dados = response.json()
        commands = dados.get("responses")
        print(commands[-1]["text"])
    else:
        raise Exception(f"Erro na requisição: {response.status_code}")
    
generate_command("Mova o robô para frente por 3 segundos.")