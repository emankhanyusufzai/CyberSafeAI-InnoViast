import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def load_system_prompt():
    try:
        with open('prompts/system_prompt.txt', 'r') as f:
            return f.read()
    except:
        return 'You are CyberSafe AI, a cybersecurity awareness assistant.'

def get_response(user_message, chat_history):
    try:
        api_key = os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=api_key)
        system_prompt = load_system_prompt()
        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash-lite',
            system_instruction=system_prompt
        )
        history = []
        for msg in chat_history:
            if msg['role'] == 'user':
                history.append({'role': 'user', 'parts': [msg['content']]})
            elif msg['role'] == 'assistant':
                history.append({'role': 'model', 'parts': [msg['content']]})
        chat = model.start_chat(history=history)
        response = chat.send_message(user_message)
        return response.text
    except Exception as e:
        error_msg = str(e)
        if '429' in error_msg or 'quota' in error_msg.lower() or 'RESOURCE_EXHAUSTED' in error_msg:
            return 'I am a little busy right now! Please wait about 30 seconds and ask me again! shield'
        elif 'API_KEY' in error_msg.upper() or 'api key' in error_msg.lower():
            return 'Oops! There is a small configuration issue. Please try again in a moment! shield'
        elif '404' in error_msg or 'not found' in error_msg.lower():
            return 'Please refresh the page and try again. shield'
        else:
            return 'Something unexpected happened! Please refresh and try again! shield'
