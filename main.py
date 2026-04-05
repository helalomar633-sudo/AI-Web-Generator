from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = "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"

class Query(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_code(query: Query):
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
               json={
                "model": "llama-3.3-70b-versatile", # هذا هو التحديث المطلوب
                "messages": [
                    {"role": "system", "content": "أنت مبرمج محترف. ردي فقط بالكود البرمجي HTML/CSS بدون أي كلام جانبي."},
                    {"role": "user", "content": query.prompt}
                ]
            }
        # فحص لو فيه خطأ جاي من Groq نفسه
        if 'choices' in result:
            ai_code = result['choices'][0]['message']['content']
            return {"code": ai_code}
        else:
            return {"error": result.get('error', {}).get('message', 'خطأ غير معروف في السيرفر')}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
