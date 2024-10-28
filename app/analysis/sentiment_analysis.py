from textblob import TextBlob

def analyze_sentiment(message: str) -> str:
    analysis = TextBlob(message)
    polarity = analysis.sentiment.polarity
    
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"
