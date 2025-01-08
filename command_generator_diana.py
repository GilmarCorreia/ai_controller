import json
import requests

main_url = ""
key = ""
name = "External-Dev"

# Get access token
url = f"{main_url}token?key={key}&accessName={name}"
response = requests.get(url, timeout=5)

print("Iniciando...")
# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    dados = response.json()  # Converte a resposta para JSON (se aplicável)
    token = dados.get("token")
    # Configura o cabeçalho de autorização com o Bearer Token
    headers = {
        "Authorization": f"Bearer {token}"
    }

    print("Token obtido com sucesso!")
else:
    raise Exception(f"Erro na requisição: {response.status_code}")

# Get session
response = requests.get(f"{main_url}session", headers=headers, timeout=5)

if response.status_code == 200:
    dados = response.json()
    session = dados.get("session")
    print("Sessão obtida com sucesso!")
else:
    raise Exception(f"Erro na requisição: {response.status_code}")

def generate_command(action):
    # Construct the prompt for the LLM
    prompt = f"""
**COMANDOS DISPONÍVEIS:**
- `'ONx'` – Liga o motor em uma velocidade analógica `x` (de 100 a 255).
- `'OFF'` – Desliga o robô.
- `'MFx'` – Move o robô para frente por `x` milissegundos.
- `'MBx'` – Move o robô para trás por `x` milissegundos.
- `'BLx'` – Pisca o LED por `x` milissegundos.
- `'CCWx'` – Gira o robô em sentido anti-horário por `x` graus.
- `'CWx'` – Gira o robô em sentido horário por `x` graus.
- `'LF'` – Ativa a função de seguidor de linha.

**REGRAS:**
0. Agora você pode definir ações detalhadas para um robô usando uma sequência de comandos específicos.
1. Quando existir os comandos `'MFx'` e `'MBx'` na resposta comece sempre com `'ONx'` e finalize com `'OFF'`.
2. Todos os valores `x` (velocidade, duração e ângulo) devem ser números positivos.
3. Todas as respostas devem conter APENAS os comandos, separados por linhas.
4. Não inclua nenhum texto adicional.

**EXEMPLOS:**
- Ação: mover para frente com velocidade máxima por 3 segundos.
- Resposta esperada:
ON255
MF3000
OFF

- Ação: piscar um LED por 3 segundos.
- Resposta esperada:
BL3000

- Ação: iniciar o robô.
- Resposta esperada:
ON255

- Ação: parar o robô.
- Resposta esperada:
OFF

- Ação: mover para trás com velocidade máxima por 5 segundos e, ao parar, piscar um LED por 3 segundos.
- Resposta esperada:
ON255
MB5000
OFF
BL3000

- Ação: girar o robô em sentido anti-horário por 90 graus.
- Resposta esperada:
CCW90

- Ação: girar o robô em sentido horário por 180 graus.
- Resposta esperada:
CW180

- Ação: ativar o seguidor de linha.
- Resposta esperada:
LF

**A SUA AÇÃO É:**
- Ação: {action}
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
        return commands[-1]["text"]
    else:
        raise Exception(f"Erro na requisição: {response.status_code}")
    
#generate_command("Mova-se em um quadrado.")
