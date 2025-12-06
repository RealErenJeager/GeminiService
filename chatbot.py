from fastapi import FastAPI
from pydantic import BaseModel
import requests, os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

app = FastAPI()

class Question(BaseModel):
    question: str


@app.post("/ask")
def ask_tech_bot(data: Question):
    question = data.question

    body = {
        "system_instruction": {
            "parts": [
                {
                    "text": (
                        "You are a strict Technology Expert. Answer questions about coding, hardware, software, and engineering only. "
                        "If a user asks about non-tech topics, politely refuse and say: 'I can only answer technology questions.'"
                    )
                }
            ]
        },
        "contents": [
            {
                "parts": [
                    {"text": question}
                ]
            }
        ]
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(URL, json=body, headers=headers)

    if response.status_code == 200:
        data = response.json()
        answer = data["candidates"][0]["content"]["parts"][0]["text"]
        return {"answer": answer}
    else:
        return {"error": "Gemini API Error", "status_code": response.status_code, "details": response.text}
