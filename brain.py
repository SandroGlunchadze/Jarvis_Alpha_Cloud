import os
import deepl
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load Keys
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
deepl_key = os.getenv("DEEPL_API_KEY")

# 2. Initialize Clients
client = OpenAI(api_key=openai_key)
translator = deepl.Translator(deepl_key)

# 3. The Senior Developer Persona (Kept from before)
system_instruction = """
ROLE:
You are Jarvis, the Senior Lead Developer and AI Architect for Sandro's Agency.
Your Project Manager is Sandro. 
Your goal is to build autonomous, bug-resistant Agentic Workflows (like "Zack").

CORE RESPONSIBILITIES:
1. CODE GENERATION: Write production-ready, modular Python code.
2. EXPLANATION: Explain 'WHY' you chose a specific library or pattern.
3. TESTING: Provide step-by-step instructions on how Sandro can test the code.
4. SCALABILITY: Always design for 10,000+ clients. Code must be efficient.
5. SELF-HEALING: Prioritize "try/except" blocks and error logging.

CONTEXT:
- We are building "Zack" (Social Media Agent) for small businesses in Georgia.
- We use Streamlit, LangChain, and OpenAI.
"""

def ask_jarvis(history):
    """
    Internal function: Talks to OpenAI in English.
    """
    try:
        messages_payload = [{"role": "system", "content": system_instruction}] + history
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=messages_payload,
            temperature=0.2,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def ask_jarvis_bilingual(user_text, chat_history):
    """
    New Wrapper: Handles the Translation Layer (Georgian <-> English).
    """
    try:
        # STEP A: Translate INBOUND (User -> English)
        # DeepL automatically detects if you wrote in Georgian.
        # target_lang="EN-US" ensures Jarvis always reads English.
        input_translation = translator.translate_text(user_text, target_lang="EN-US")
        english_text = input_translation.text
        source_lang = input_translation.detected_source_lang
        
        # Debug print to see what happens in the terminal
        print(f"Original: {user_text} | Detected: {source_lang} | English: {english_text}")

        # STEP B: Talk to Jarvis (in English)
        # We append the translated English text to history temporarily for processing
        temp_history = chat_history + [{"role": "user", "content": english_text}]
        jarvis_reply_english = ask_jarvis(temp_history)

        # STEP C: Translate OUTBOUND (English -> User)
        # Logic: If you spoke Georgian (KA), Jarvis replies in Georgian (KA).
        # If you spoke English (EN), Jarvis replies in English (EN).
        
        if source_lang == "KA":
            output_translation = translator.translate_text(jarvis_reply_english, target_lang="KA")
            final_reply = output_translation.text
        else:
            # If you wrote in English (or anything else), he keeps it English.
            final_reply = jarvis_reply_english

        return final_reply, english_text

    except Exception as e:
        return f"Translation Error: {e}", user_text