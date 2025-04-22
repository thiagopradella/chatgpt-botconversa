from fastapi import FastAPI, Request
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# Configura a chave da API
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

@app.post("/webhook")
async def receber_webhook(request: Request):
    data = await request.json()
    mensagem = data.get("mensagem", "")
    fluxo = data.get("fluxo", "")
    etapa = data.get("etapa", "")

    resposta = gerar_resposta_chatgpt(mensagem, fluxo, etapa)
    return {"response": resposta}

def gerar_resposta_chatgpt(mensagem: str, fluxo: str, etapa: str) -> str:
    prompt = (
        f"O usuário no fluxo '{fluxo}' na etapa '{etapa}' disse: {mensagem}\n"
        "Responda de forma objetiva e clara:"
    )

    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente jurídico atencioso."},
            {"role": "user", "content": prompt}
        ]
    )

    return resposta.choices[0].message.content
