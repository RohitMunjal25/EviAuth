import tensorflow as tf
import numpy as np
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(current_dir, "cifake.keras")

try:
    print(" Loading GenAI (CIFAKE) Model...")
    genai_model = tf.keras.models.load_model(MODEL_PATH)
    print("GenAI Detector Loaded Successfully!")
except Exception as e:
    print(f" Error: 'cifake.keras' load nahi hua! Kripya check karein ki wo models folder mein hai ya nahi.")
    print(f"Details: {e}")
    genai_model = None

def detect_ai_generated(file_path):
    if genai_model is None:
        return {"genai_score": 0.0, "status": "Model Missing"}

    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Image not found at {file_path}")

        img = tf.keras.utils.load_img(file_path, target_size=(224, 224))
        img_array = tf.keras.utils.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        
        # ==========================================
        # FIX: Normalize the image pixels to 0-1 range
        # ==========================================
        img_array = img_array / 255.0
        
        prediction = genai_model.predict(img_array, verbose=0)
        
        score = float(prediction[0][0]) * 100

        return {
            "genai_score": round(score, 2),
            "status": "AI Generated" if score > 50 else "Real"
        }
        
    except Exception as e:
        print(f"GenAI Analysis Error: {e}")
        return {"genai_score": 0.0, "status": "Error"}

if __name__ == "__main__":
    print("Run this script via app.py or provide a test image path below.")