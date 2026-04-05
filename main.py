from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests # هنستخدم طريقة بسيطة للربط

app = FastAPI()

# عشان الموقع يقدر يكلم الكود ده
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_code(request: UserRequest):
    # هنا هنحط مفتاح الـ API اللي هنجيبه من Groq أو OpenAI
    # حالياً هخلي الكود يرجع رسالة تجريبية عشان نتأكد إن الربط شغال
    print(f"وصلني طلب لعمل موقع: {request.prompt}")
    return {"code": f"تم استلام طلبك لعمل: {request.prompt}\nجارٍ تجهيز الأكواد بدقة 100%..."}

if __name__ == "__main__":
    import uvicorn
    print("المحرك اشتغل! روح افتح ملف index.html وجرب تكتب حاجة")
    uvicorn.run(app, host="127.0.0.1", port=8000)
