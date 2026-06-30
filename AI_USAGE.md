# AI Usage Documentation — CyberSafe AI

## Project Overview
CyberSafe AI is a chatbot built for the InnoViast Week 1 — AI Solutions Engineering Assignment. It helps everyday users understand cybersecurity concepts (passwords, phishing, malware, privacy, etc.) in simple, beginner-friendly language.

## Tools & Technologies Used
- Frontend/UI: Streamlit
- AI Model: Google Gemini (gemini-2.5-flash) via google-generativeai SDK
- Knowledge Base: Custom PDF (50 FAQs) loaded using PyPDF2
- Environment Management: python-dotenv (.env file for API key security)
- Language: Python 3.14

## System Prompt Design
The chatbot uses a strict system prompt (see prompts/system_prompt.txt) that:
- Defines the persona as a friendly, beginner-friendly cybersecurity educator
- Restricts answers strictly to cybersecurity-related topics
- Refuses out-of-scope questions (e.g. sports, marketing, cooking) with a polite fallback message
- Enforces short, concise answers (3-6 lines) for better readability
- Includes ethical boundaries — never assists with hacking, malware creation, or illegal activity

## Key Manual Improvements Made
While AI tools were used to help generate and debug code, the following decisions and refinements were made manually:
- Designed and refined the dark cyber-themed UI (colors, layout, WhatsApp-style chat bubbles)
- Built a custom Risk Checker feature that classifies user messages into Low/Medium/High risk based on keyword detection (e.g. detecting if a user shared an OTP or clicked a suspicious link)
- Created a 50-question FAQ PDF knowledge base covering 12 cybersecurity categories
- Fixed UI alignment issues (input bar and send button layout, sidebar visibility)
- Tested and validated scope-limiting behavior with multiple out-of-scope queries
- Implemented error handling for empty input, long input, and API failures

## Limitations
- Uses Google Gemini's free tier, which has a daily request quota — may temporarily stop responding if quota is exceeded
- Knowledge is limited to the topics covered in the FAQ PDF and the model's general training; it does not have real-time threat intelligence
- Not a replacement for professional cybersecurity consultation — for serious incidents, users are advised to contact a professional

## Data Ethics & Privacy
- No user conversation data is stored or logged anywhere
- API key is stored only in a local .env file and is excluded from GitHub via .gitignore
- The app does not collect, save, or share any personal information from users