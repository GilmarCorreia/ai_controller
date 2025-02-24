import os
import time
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

# ID do seu Assistant criado no painel da OpenAI
assistant_id = "asst_BB2fNJswIccw6497MikuLe7N"

def generate_command(interaction):
    # Criando uma thread para interagir com o Assistant
    thread = openai.beta.threads.create()

    # Enviando uma mensagem ao Assistant
    message = openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=interaction
    )

    # Executando o Assistant para processar a mensagem
    run = openai.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    # Verificando a resposta
    while run.status != "completed":
        #time.sleep(1)
        run = openai.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

    # Pegando a resposta gerada pelo Assistant
    messages = openai.beta.threads.messages.list(thread_id=thread.id)

    return messages.data[0].content[0].text.value
    #print(messages.data[0].content[0].text.value)
