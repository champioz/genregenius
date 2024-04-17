from sentence_transformers import SentenceTransformer
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from joblib import load
from datetime import datetime
import streamlit

def classify_input(input_description:str) -> str:
    embed_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    RFmod = load('./public/scripts/rfc.joblib')

    embedded = embed_model.encode(input_description)
    embedded = np.pad(embedded, (0, 768 - len(embedded)), 'constant').reshape(1,-1)
    
    label = RFmod.predict(embedded)
    return str(label[0])


