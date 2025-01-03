import os
from dotenv import load_dotenv
import google.generativeai as genai

def initialize_llm():
    load_dotenv()
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    generation_config = {
    'temperature': 0.1,      # Lower value for more deterministic responses
    'top_p': 0.5,           # More focused sampling
    'top_k': 10,            # Limit token selection
    'max_output_tokens': 100 # Control response length
    }

    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    }
    ]

    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash-8b',
        generation_config=generation_config,
        safety_settings=safety_settings
    )

    return model.start_chat()