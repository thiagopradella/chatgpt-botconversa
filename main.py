from fastapi import FastAPI, Request
import openai
import requests
import os

app = FastAPI()

# Pegando as chaves das variáveis de ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")
BOTCONVERSA_TOKEN = os.getenv("BOTCONVERSA_TOKEN")

# Função que envia a pergunta ao ChatGPT
def gerar_resposta_chatgpt(mensagem_usuario, fluxo, etapa):
    prompt = f"""
Você é um assistente virtual que está conversando com um cliente no fluxo "{fluxo}", etapa {etapa}.
Mensagem do cliente: "{mensagem_usuario}"

Baseado nisso, responda de forma simpática e direta, guiando o usuário para a próxima etapa do fluxo.
"""
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return resposta.choices[0].message.content.strip()

# Rota que o BotConversa vai chamar
@app.post("/webhook")
async def receber_webhook(request: Request):
    data = await request.json()

    mensagem = data.get("mensagem", "")
    numero = data.get("numero", "")
    fluxo = data.get("fluxo", "Desconhecido")
    etapa = data.get("etapa", "1")

    resposta = gerar_resposta_chatgpt(mensagem, fluxo, etapa)

    # Enviando a resposta de volta ao BotConversa
    requests.post(
        "https://api.botconversa.com.br/api/v1/mensagem",
        json={
            "numero": numero,
            "mensagem": resposta,
            "token": BOTCONVERSA_TOKEN
        }
    )

    return {"status": "ok", "resposta": resposta}
