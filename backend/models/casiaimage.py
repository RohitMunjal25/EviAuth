import cv2
import numpy as np
from tensorflow.keras.models import load_model

MODEL_PATH = "models/casia_model.h5"

try:
    casia_model = load_model(MODEL_PATH)
except Exception as e:
    print(f"❌ Error loading CASIA model: {e}")
    casia_model = None

def detect_casia_fake(img_path):
    if casia_model is None:
        return {"casia_score": 0.0, "casia_label": "Model Not Loaded"}

    img = cv2.imread(img_path)
    if img is None:
        return {"casia_score": 0.0, "casia_label": "Invalid Image"}

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    try:
        try:
            shape = casia_model.input_shape
            target_shape = (shape[1], shape[2])
        except:
            target_shape = (224, 224) 

        img_resized = cv2.resize(img_rgb, target_shape)
        img_ready = np.expand_dims(img_resized.astype("float32") / 255.0, axis=0)

        pred = casia_model.predict(img_ready, verbose=0)[0][0]
        
        real_confidence = float(pred * 100)
        fake_score = 100.0 - real_confidence 

        return {
            "casia_score": round(fake_score, 2),
            "casia_label": "Manipulated" if fake_score > 65 else "Authentic"
        }
    except Exception as e:
        print(f"❌ CASIA Processing Error: {e}")
        return {"casia_score": 0.0, "casia_label": "Error"}