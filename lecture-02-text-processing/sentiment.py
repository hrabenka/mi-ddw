import os

from nltk.sentiment import SentimentIntensityAnalyzer

text = None
with open(os.path.join(os.path.dirname(__file__), 'message.txt'), 'r') as f:
    text = f.read()

vader_analyzer = SentimentIntensityAnalyzer()

sentiment = vader_analyzer.polarity_scores(text)
print("Sentiment:")
print(sentiment)
