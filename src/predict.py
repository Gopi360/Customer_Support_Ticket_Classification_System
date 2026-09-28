import re
import joblib

vectorizer = joblib.load('model/vectorizer.pkl')
model = joblib.load('model/classifier.pkl')

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\{.*?\}', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return re.sub(r'\s+', ' ', text).strip()

def predict_category(description):
    features = vectorizer.transform([clean_text(description)])
    probs = model.predict_proba(features)[0]
    idx = probs.argmax()
    return model.classes_[idx], probs[idx] * 100

if __name__ == "__main__":
    text = input("Enter Ticket Description:\n> ")
    category, conf = predict_category(text)
    print(f"Predicted Category: {category}")
    print(f"Confidence: {conf:.1f}%")