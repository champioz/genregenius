from sentence_transformers import SentenceTransformer
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from joblib import load
from datetime import datetime
import streamlit

def classify_input(input_description:str) -> str:
    embed_model = SentenceTransformer('all-mpnet-base-v2')
    RFmod = load('./public/scripts/xgboost.pkl')

    embedded = embed_model.encode(input_description)
    embedded = np.pad(embedded, (0, 768 - len(embedded)), 'constant').reshape(1,-1)
    
    label = RFmod.predict(embedded)
    return str(label[0])


