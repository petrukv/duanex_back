from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.analysis.sentiment_analysis import analyze_sentiment
from app.gemini.gemini_response import generate_gemini_response
from app.schemas.message_schema import MessageRequest

app = FastAPI()
interaction_count = 0  # змінна для підрахунку взаємодій з користувачем

origins = [
    "http://localhost",
    "https://localhost",
    'http://127.0.0.1:5500',
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Базова обробка для привітань та прощань
def basic_conversation(message: str) -> str:
    greetings = ["hello", "hi", "hey"]
    farewells = ["bye", "goodbye", "see you"]

    lower_message = message.lower()
    if any(greet in lower_message for greet in greetings):
        return "Hi! How can I assist you today?"
    elif any(farewell in lower_message for farewell in farewells):
        return "Goodbye! Have a great day!"
    return None

# Основний маршрут для обробки повідомлень
@app.post("/response")
def generate_response(request: MessageRequest):
    global interaction_count
    try:
        # Перевірка на прості запити
        basic_reply = basic_conversation(request.message)
        if basic_reply:
            return {"response": basic_reply}
        
        # Аналіз настрою повідомлення
        sentiment = analyze_sentiment(request.message)

        # Генерація відповіді
        response_text = generate_gemini_response(request.message)

        # Налаштування відповіді на основі настрою
        if sentiment == "positive":
            response_text = "I'm glad to hear that! 😊 (positive) " + response_text
        elif sentiment == "negative":
            response_text = "I'm sorry you're facing issues. 😔 (negative) " + response_text
        elif sentiment == "neutral":
            response_text = response_text + "Alright! How can I assist you further? (neutral) "

        # Збільшення лічильника взаємодій
        interaction_count += 1

        # Запит зворотного зв’язку після кожних трьох взаємодій
        if interaction_count % 3 == 0:
            response_text += " By the way, could you provide some feedback on our conversation?"

        return {"response": response_text, "sentiment": sentiment}

    except ValueError as e:
        raise HTTPException(status_code=500, detail="I'm not sure I understand that. Could you please rephrase?")

