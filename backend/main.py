from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

# IMPORTANT: To use a real AI, uncomment these lines and configure your API key
# import google.generativeai as genai
# import os
# genai.configure(api_key="YOUR_GEMINI_API_KEY_HERE")
# model = genai.GenerativeModel('gemini-pro')

app = FastAPI(title="DentAssist API")

# Enable CORS for the frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with your actual website URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic system prompt for the AI
SYSTEM_PROMPT = """
You are DentAssist, a warm and professional AI dental assistant for Navadiya Dental Clinic in Surat, Gujarat.

[... Full Prompt omitted in this basic mock. In a real AI implementation, 
this prompt would be passed as a system instruction to the LLM ...]

Tone: Warm, friendly, reassuring — never cold or robotic.
Language: STRICTLY ENGLISH ONLY. Do not use Hindi or Hinglish.
NEVER diagnose — always say "Please consult with the doctor to confirm."
"""

class Message(BaseModel):
    role: str # 'user' or 'bot'
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[Message] = []

@app.get("/")
def health_check():
    return {"status": "ok", "message": "DentAssist API is running!"}

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    user_msg = request.message.lower()
    
    # ==========================================
    # --- REAL AI IMPLEMENTATION (GEMINI EXAMPLE) ---
    # ==========================================
    # try:
    #     # Convert history to Gemini format (example)
    #     chat = model.start_chat()
    #     response = chat.send_message(f"SYSTEM: {SYSTEM_PROMPT}\nUSER: {user_msg}")
    #     return {"reply": response.text}
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
    # ==========================================
    
    # ==========================================
    # --- MOCK LOGIC FOR DEMONSTRATION ---
    # Since we need to run this instantly without an API key, 
    # here is a simple mock logic based on the user's intent.
    # ==========================================
    dental_keywords = ["tooth", "teeth", "pain", "dentist", "appointment", "clinic", "clean", "root canal", "crown", "braces", "aligners", "hurt", "doctor", "gum", "bleed", "cost", "price", "fee", "time", "hours", "where", "location", "address", "hello", "hi", "hey", "treatment", "implant", "extract", "booking", "number", "call"]
    
    # Check if the query is related to dentistry based on keywords
    is_dental_query = any(word in user_msg for word in dental_keywords)

    if not is_dental_query:
        reply = "I am DentAssist, a specialized AI for Navadiya Dental Clinic. I can only answer questions related to dental care, our services, or booking an appointment. How can I help you with your smile today? 🦷"
    else:
        if any(word in user_msg for word in ["appointment", "book", "schedule", "visit"]):
            reply = "To book an appointment, please call or WhatsApp Dr. Navadia directly at: **📞 +91 94279 68553**. Our reception will assist you with the booking. What treatment are you looking to schedule?"
        elif any(word in user_msg for word in ["number", "contact", "call"]):
            reply = "You can reach Navadiya Multispeciality Dental Clinic by calling us at: **📞 +91 94279 68553**. We are happy to help!"
        elif any(word in user_msg for word in ["severe pain", "swelling", "bleeding", "broken", "accident", "emergency"]):
            reply = "This sounds like a dental emergency! 🚨 Please call us immediately at **📞 +91 94279 68553**. Dr. Jatin and Dr. Dimpal are available to help. Please don't panic, we are here for you!"
        elif any(word in user_msg for word in ["cost", "price", "fee", "how much", "charges"]):
            reply = ("Here is a rough idea of our treatment prices:\n"
                     "• **Consultation & Checkup:** ₹300 - ₹500\n"
                     "• **Teeth Cleaning (Scaling):** ₹500 - ₹1,200\n"
                     "• **Tooth Extraction:** ₹500 - ₹2,000 (Surgical extractions cost more)\n"
                     "• **Root Canal Treatment (RCT):** ₹3,000 - ₹6,000 per tooth\n"
                     "• **Dental Crowns/Caps:** ₹2,500 - ₹10,000 (Depends on material like Zirconia/Ceramic)\n"
                     "• **Dental Implants:** Starts from ₹20,000\n"
                     "• **Braces/Aligners:** Starts from ₹25,000\n\n"
                     "Please note these are just rough estimates. The exact cost depends on your clinical checkup. Would you like our doctor's number to book a checkup?")
        elif any(word in user_msg for word in ["time", "hours", "open", "saturday"]):
            reply = "We are open Monday to Saturday, from **09:30 AM to 09:30 PM**. On Sundays, we are open from **09:30 AM to 02:00 PM**. ⏰"
        elif any(word in user_msg for word in ["where", "address", "location"]):
            reply = "Our clinic is located at **304, Sunshine Plaza, Katargam, Surat, Gujarat**. 🚗"
        elif "hurt" in user_msg or "painless" in user_msg or "pain" in user_msg:
            reply = "A regular checkup is completely painless! For procedures like Root Canals or Extractions, we use local anesthesia so you will be completely numb and comfortable. 😊"
        elif "hello" in user_msg or "hi" in user_msg or "hey" in user_msg:
            reply = "Hello! 👋 I am DentAssist, the AI assistant for Navadiya Dental Clinic. How can I help you regarding your dental health today? 🦷"
        else:
            reply = "That's a great question about dental health! While I am a digital assistant providing general information, our expert dentists can provide a full consultation. To book an appointment, please call **📞 +91 94279 68553**."
            
    return {"reply": reply}

if __name__ == "__main__":
    import uvicorn
    # Run development server
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
