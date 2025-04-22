from fastapi import FastAPI, Request
import openai
import os

app = FastAPI()

# Configure sua chave da OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/webhook")
async def receber_webhook(request: Request):
    data = await request.json()
    root = data.get("root", {})  # pega o conteúdo do campo 'root'
    
    mensagem = root.get("mensagem", "")
    numero = root.get("numero", "")
    fluxo = root.get("fluxo", "")
    etapa = root.get("etapa", "")

    resposta = gerar_resposta_chatgpt(mensagem, fluxo, etapa)

    return {"response": resposta}

def gerar_resposta_chatgpt(mensagem: str, fluxo: str, etapa: str) -> str:
    prompt = (
        f"Usuário no fluxo '{fluxo}' na etapa '{etapa}' disse: {mensagem}.\n"
        f"Responda de forma clara, objetiva e amigável:"
    )

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente jurídico atencioso."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()
