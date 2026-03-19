import fitz  # PyMuPDF
import tensorflow as tf
import numpy as np
from PIL import Image, ImageChops, ImageEnhance
import io
import os

MODEL_PATH = os.path.join(os.getcwd(),"models", "midv500.keras")
model = tf.keras.models.load_model(MODEL_PATH)

def apply_ela(img, quality=90):
    temp_io = io.BytesIO()
    img.save(temp_io, 'JPEG', quality=quality)
    temp_io.seek(0)
    temp_img = Image.open(temp_io)
    ela_img = ImageChops.difference(img, temp_img)
    extrema = ela_img.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0: max_diff = 1
    scale = 255.0 / max_diff
    return ImageEnhance.Brightness(ela_img).enhance(scale)

def detect_document_fake(file_path):
    doc = fitz.open(file_path)
    page_results = []
    
    for i in range(len(doc)):
        page = doc.load_page(i)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img_data = pix.tobytes("png")
        original_img = Image.open(io.BytesIO(img_data)).convert('RGB')

        # AI Prediction on Original
        img_resized = original_img.resize((224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img_resized)
        img_array = np.expand_dims(img_array, axis=0)
        orig_score = float(model.predict(img_array, verbose=0)[0][0])

        # AI Prediction on ELA
        ela_img = apply_ela(original_img)
        ela_resized = ela_img.resize((224, 224))
        ela_array = tf.keras.preprocessing.image.img_to_array(ela_resized)
        ela_array = np.expand_dims(ela_array, axis=0)
        ela_score = float(model.predict(ela_array, verbose=0)[0][0])

        # Hybrid Score (Average)
        final_page_score = (orig_score + ela_score) / 2
        page_results.append(final_page_score)

    doc.close()
    
    # Poore document ka average score nikaalo
    avg_doc_score = sum(page_results) / len(page_results)
    
    return {
        "doc_score": round(avg_doc_score * 100, 2), 
        "total_pages": len(page_results),
        "raw_scores": page_results
    }