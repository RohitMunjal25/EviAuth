import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model

MODEL_PATH = "models/dfdc_model.h5"
model = load_model(MODEL_PATH)

def preprocess(img):
    if img is None or img.size == 0:
        return None
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def detect_deepfake(frames_folder):
    scores = []
    abs_folder = os.path.abspath(frames_folder)
    
    for f in os.listdir(abs_folder):
        path = os.path.join(abs_folder, f)
        img = cv2.imread(path)
        if img is None: continue
        
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_ready = preprocess(img_rgb)
        
        if img_ready is not None:
            pred = model.predict(img_ready, verbose=0)[0][0]
            fake_prob = 1.0 - float(pred) 
            scores.append(fake_prob)

    if not scores:
        return {"deepfake_score": 0.0, "deepfake_label": "Analysis Failed"}

    avg_fake_score = sum(scores) / len(scores)
    final_score = float(round(avg_fake_score * 100, 2))
    
    return {
        "deepfake_score": final_score, 
        "deepfake_label": "Deepfake" if final_score >= 50 else "Real"
    }