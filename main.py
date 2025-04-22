from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os

from openai import OpenAI

app = FastAPI()

# Configura chave da API
openai.api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

@app.post("/webhook")
async def receber_webhook(request: Request):
    data = await request.json()
    mensagem = data.get("mensagem", "")
    fluxo = data.get("fluxo", "")
    etapa = data.get("etapa", "")

    resposta = gerar_resposta_chatgpt(mensagem, fluxo, etapa)

    return {"response": resposta}

def gerar_resposta_chatgpt
return resposta.choices[0].message.content

