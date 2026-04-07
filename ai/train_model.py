import pandas as pd
import io
import requests
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import jobit # To save the model for your FastAPI app

# --- STEP 1: LOAD UCI GLOBAL DATASET ---
def load_global_data():
    url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
    # Using a known mirror for the UCI SMS dataset for speed
    df = pd.read_csv(url, sep='\t', header=None, names=['label', 'text'])
    df['label'] = df['label'].map({'spam': 1, 'ham': 0})
    return df

# --- STEP 2: ADD MALAYSIAN BNM SAMPLES ---
def get_local_samples():
    local_data = [
        {"text": "RM0 PTPTN: Waran tangkap dikeluarkan. Sila bayar di https://ptptn-gov.me", "label": 1},
        {"text": "Tahniah! Mata ganjaran CIMB anda tamat hari ini. Tebus di: https://cimb-rewards.net", "label": 1},
        {"text": "LHDN: Anda ada bayaran balik cukai RM850.70. Klik: http://lhdn-refund.org", "label": 1},
        {"text": "PENGUMUMAN: Pemenang bertuah Shopee RM3,000! WhatsApp: 011-23456789", "label": 1},
        {"text": "Wei, jadi ke nak lepak mamak malam ni?", "label": 0},
        {"text": "Mak, adik dah sampai TBS ni. Tengah tunggu Grab.", "label": 0},
        {"text": "Boleh tolong approve kawan punya logbook internship tak?", "label": 0}
    ]
    return pd.DataFrame(local_data)

# --- STEP 3: TRAIN THE HYBRID MODEL ---
def train_hybrid_model():
    print("Merging datasets...")
    global_df = load_global_data()
    local_df = get_local_samples()
    
    # Combine (Local samples are repeated 10x to give them more weight)
    final_df = pd.concat([global_df, local_df] * 10, ignore_index=True)
    
    # Text vectorization + Classifier Pipeline
    # TF-IDF turns words into numbers that the computer understands
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2), stop_words=None)), 
        ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        final_df['text'], final_df['label'], test_size=0.2
    )

    print("Training model...")
    pipeline.fit(X_train, y_train)
    
    score = pipeline.score(X_test, y_test)
    print(f"✅ Model Accuracy: {score * 100:.2f}%")

    # Save the model and vectorizer
    joblib.dump(pipeline, 'ai/scam_model.pkl')
    print("🚀 Model saved as ai/scam_model.pkl")

if __name__ == "__main__":
    train_hybrid_model()