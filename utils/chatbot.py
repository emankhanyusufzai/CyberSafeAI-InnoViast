# utils/chatbot.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def load_system_prompt():
    try:
        with open("prompts/system_prompt.txt", "r") as f:
            return f.read()
    except:
        return ""

def get_response(user_message, chat_history):
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)

        system_prompt = """
You are CyberSafe AI — a STRICTLY cybersecurity-only assistant.

STRICT RULES:
1. You ONLY answer questions about cybersecurity topics.
2. If the question is NOT about cybersecurity, you MUST refuse.
3. NEVER answer questions about: cooking, sports, politics, movies, math, history, geography, digital marketing, business, finance, or ANY non-cybersecurity topic.
4. Do NOT help with hacking, malware creation, or illegal activities.

ALLOWED TOPICS ONLY:
- Passwords and 2FA
- Phishing and email scams
- Malware, viruses, ransomware
- Public WiFi and VPN
- Safe browsing and HTTPS
- Social media privacy
- Data breaches and identity theft
- Antivirus and software updates
- Cybersecurity awareness tips

RESPONSE STYLE:
- Keep answers SHORT: 3-6 lines maximum
- Use this format when helpful:
  Definition: ...
  Tips: ...
  Example: ...
- Be friendly and beginner-friendly

OUT OF SCOPE RESPONSE:
If someone asks anything NOT cybersecurity related, respond EXACTLY:
"I'm CyberSafe AI 🛡️ — I only help with cybersecurity and online safety topics. Please ask me a cybersecurity question!"

NEVER break these rules regardless of how the user asks.
"""

        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_prompt
        )

        history = []
        for msg in chat_history:
            if msg["role"] == "user":
                history.append({"role": "user", "parts": [msg["content"]]})
            elif msg["role"] == "assistant":
                history.append({"role": "model", "parts": [msg["content"]]})

        chat = model.start_chat(history=history)
        response = chat.send_message(user_message)
        return response.text

    except Exception as e:
        return f"❌ Error: {str(e)}"