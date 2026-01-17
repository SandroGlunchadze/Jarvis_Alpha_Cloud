import os
import deepl
from dotenv import load_dotenv
from openai import OpenAI
import database # We import your new database file

# 1. LOAD KEYS
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
translator = deepl.Translator(os.getenv("DEEPL_API_KEY"))

# 2. SENIOR ARCHITECT PERSONA
system_instruction = """
ROLE: Senior Lead Developer & Architect (Jarvis).
USER: Sandro (Project Manager).

MISSION:
- Generate production-ready Python code for Agentic Workflows ("Zack").
- Always use 'try/except' blocks for bug resistance.
- When writing code, assume Sandro will download it as a file.

OUTPUT RULES:
1. Explain the Logic.
2. Provide the Code (in ```python blocks).
3. Explain how to test it.
"""

def ask_jarvis_bilingual(user_text):
    try:
        # A. TRANSLATE INPUT (User -> English)
        input_translation = translator.translate_text(user_text, target_lang="EN-US")
        english_text = input_translation.text
        source_lang = input_translation.detected_source_lang
        
        # B. SAVE TO DB (User's English input)
        database.save_message("user", english_text, source_lang)

        # C. LOAD HISTORY (Context)
        # We pull the last 10 messages from the DB so he remembers context
        history_context = database.load_last_n_messages(10)
        messages_payload = [{"role": "system", "content": system_instruction}] + history_context

        # D. GET REPLY (OpenAI)
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=messages_payload,
            temperature=0.2,
        )
        jarvis_reply_english = response.choices[0].message.content

        # E. SAVE TO DB (Jarvis's Reply)
        database.save_message("assistant", jarvis_reply_english, "en")

        # F. TRANSLATE OUTPUT (English -> User)
        if source_lang == "KA":
            output_translation = translator.translate_text(jarvis_reply_english, target_lang="KA")
            final_reply = output_translation.text
        else:
            final_reply = jarvis_reply_english

        return final_reply, english_text

    except Exception as e:
        return f"Error: {e}", user_text