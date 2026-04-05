from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests # تأكدنا إننا حملنا المكتبة دي بـ pip install requests

app = FastAPI()

# السماح للمتصفح بالاتصال بالمحرك
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ضع مفتاحك السري هنا
GROQ_API_KEY = "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"

class Query(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_code(query: Query):
    try:
        # إرسال الطلب لذكاء Groq الاصطناعي
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "system", "content": "أنت مبرمج محترف. ردي فقط بالكود البرمجي (HTML/CSS/JS) لأي موقع يطلبه المستخدم بدون مقدمات."},
                    {"role": "user", "content": query.prompt}
                ]
            }
        )
        
        result = response.json()
        ai_code = result['choices'][0]['message']['content']
        
        return {"code": ai_code}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("المحرك اشتغل بالذكاء الاصطناعي! جرب الآن من المتصفح.")
    uvicorn.run(app, host="127.0.0.1", port=8000)
