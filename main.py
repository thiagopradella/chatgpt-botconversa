from fastapi import FastAPI, Request
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/webhook")
async def receber_webhook(request: Request):
    data = await request.json()
    
    root = data.get("root", {})
    
    mensagem = root.get("mensagem", "")
    fluxo = root.get("fluxo", "")
    etapa = root.get("etapa", "")
    numero = root.get("numero", "")
    
    resposta = gerar_resposta_chatgpt(mensagem, fluxo, etapa, numero)
    
    return {"response": resposta}

def gerar_resposta_chatgpt(mensagem: str, fluxo: str, etapa: str, numero: str) -> str:
    prompt = (
        f"O usuário com número {numero}, no fluxo '{fluxo}' e na etapa '{etapa}', "
        f"disse: {mensagem}\nResponda de forma clara e objetiva."
    )
    
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente jurídico cordial e claro."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return resposta.choices[0].message.content
