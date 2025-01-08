from openai import OpenAI
client = OpenAI()
def generate_command(action):
    # Construct the prompt for the LLM

#----- Examples -----
#     - Action: move forward with max speed for 3 seconds
#     - Response: ON255|MF3000|OFF

#     - Action: Start running
#     - Response: ON255

#     - Action: Stop running
#     - Response: OFF
    prompt = f"""
**INSTRUÇÕES:**
0. Agora você pode definir ações detalhadas para um robô usando uma sequência de comandos específicos.
1. Quando existir os comandos `'MFx'` e `'MBx'` na resposta comece sempre com `'ONx'` e finalize com `'OFF'`.
2. Todos os valores `x` (velocidade, duração e ângulo) devem ser números positivos.
3. Todas as respostas devem conter APENAS os comandos, separados por linhas.
4. Não inclua nenhum texto adicional.

**COMANDOS DISPONÍVEIS:**
- `'ONx'` – Liga o motor em uma velocidade analógica `x` (de 100 a 255).
- `'OFF'` – Desliga o robô.
- `'MFx'` – Move o robô para frente por `x` milissegundos.
- `'MBx'` – Move o robô para trás por `x` milissegundos.
- `'BLx'` – Pisca o LED por `x` milissegundos.
- `'CCWx'` – Gira o robô em sentido anti-horário por `x` graus.
- `'CWx'` – Gira o robô em sentido horário por `x` graus.
- `'LF'` – Ativa a função de seguidor de linha.

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

    try:
        # Call the OpenAI API to get a command
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the command from the response
        return completion.choices[0].message.content

    except Exception as e:
        return f"An error occurred: {e}"
