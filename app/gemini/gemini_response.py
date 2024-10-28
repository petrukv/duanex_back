import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY')

genai.configure(api_key=api_key)

def generate_gemini_response(message: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(message)
        
        if not response or not response.text:
            raise ValueError("Gemini не повернула відповідь")

        # Видалення символів переносу рядка
        return response.text.replace("\n", " ")
    
    except Exception as e:
        raise ValueError(f"Помилка під час генерації відповіді: {str(e)}")