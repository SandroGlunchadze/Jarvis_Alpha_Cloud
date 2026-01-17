import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load the secret key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# 2. Define Personality
system_instruction = """
You are Jarvis, an advanced AI support system for small businesses.
Your tone is professional, concise, and helpful.
You act as a strategic partner to Sandro.
"""

def ask_jarvis(history):
    """
    New Function: Accepts a LIST of messages (history), not just one text.
    """
    try:
        # We put the System Instruction at the very top of the list
        messages_payload = [{"role": "system", "content": system_instruction}] + history
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages_payload,
            temperature=0.7,
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error: {e}"