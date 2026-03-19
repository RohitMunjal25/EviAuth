import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from mtcnn import MTCNN 

MODEL_PATH = "models/faceforensics_model.h5"
try:
    model = load_model(MODEL_PATH)
except Exception as e:
    print(f"Error loading FaceForensics model: {e}")

detector = MTCNN() 

def detect_faceforensics(frames_folder):
    scores = []
    target_h, target_w = 160, 160 
    abs_folder = os.path.abspath(frames_folder)

    for f in os.listdir(abs_folder):
        path = os.path.join(abs_folder, f)
        img = cv2.imread(path)
        if img is None: 
            continue

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        try:
            results = detector.detect_faces(img_rgb)
            
            if not results:
                continue

            res = results[0]
            if 'box' not in res or len(res['box']) < 4:
                continue

            x, y, w, h = res['box']
            if w <= 0 or h <= 0:
                continue

            start_x, start_y = max(0, x), max(0, y)
            end_x, end_y = start_x + w, start_y + h
            
            face = img_rgb[start_y:end_y, start_x:end_x]
            
            if face.size == 0 or face.shape[0] == 0 or face.shape[1] == 0:
                continue

            face_resized = cv2.resize(face, (target_w, target_h))
            face_ready = np.expand_dims(face_resized.astype("float32") / 255.0, axis=0)
            
            if face_ready.shape == (1, 160, 160, 3):
                pred = model.predict(face_ready, verbose=0)[0][0]
                fake_prob = 1.0 - float(pred)
                scores.append(fake_prob)
            
        except Exception as e:
            print(f"Bypassing internal error for frame {f}: {e}")
            continue

    if not scores:
        return {"ff_score": 0.0, "ff_label": "No Face Detected"}

    avg_fake_prob = sum(scores) / len(scores)
    return {
        "ff_score": float(round(avg_fake_prob * 100, 2)),
        "ff_label": "Deepfake" if avg_fake_prob > 0.65 else "Real" 
    }