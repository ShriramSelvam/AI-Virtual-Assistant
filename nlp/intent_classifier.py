import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load intents
with open("data/intents.json") as f:
    intents = json.load(f)

texts = []
labels = []

for intent, examples in intents.items():
    for example in examples:
        texts.append(example)
        labels.append(intent)

# Vectorize text
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

# Train classifier
model = LogisticRegression()
model.fit(X, labels)

def predict_intent(text):
    vec = vectorizer.transform([text])
    return model.predict(vec)[0]
