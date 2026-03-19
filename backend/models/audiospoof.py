import librosa
import numpy as np
import tensorflow as tf
import os
import warnings

warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

class SafeDense(tf.keras.layers.Dense):
    def __init__(self, **kwargs):
        kwargs.pop('quantization_config', None)
        super().__init__(**kwargs)

print(" Booting Audio Forensics Models...")

try:
    pa_model = tf.keras.models.load_model('models/asvspoof_pa_model.h5', custom_objects={'Dense': SafeDense}, compile=False) 
    la_model = tf.keras.models.load_model('models/asvspoof_la_model.h5', custom_objects={'Dense': SafeDense}, compile=False) 
    print(" LA & PA Audio Engines Online!\n")
except Exception as e:
    print(f" Bhai Model loading me error aaya: {e}")

def auto_prepare_audio(audio_path, target_shape):
    y, sr = librosa.load(audio_path, sr=16000)
    
    if len(target_shape) == 3:
        length = target_shape[1] if target_shape[1] is not None else 64000
        y = y[:length] if len(y) > length else np.pad(y, (0, length - len(y)))
        return np.reshape(y, (1, length, 1))

    elif len(target_shape) == 4:
        h = target_shape[1] if target_shape[1] is not None else 128
        w = target_shape[2] if target_shape[2] is not None else 128
        
        target_len = w * 512
        y = y[:target_len] if len(y) > target_len else np.pad(y, (0, target_len - len(y)))
            
        mels = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=2048, hop_length=512, n_mels=h)
        mels_db = librosa.power_to_db(mels, ref=np.max)
        mels_db = mels_db[:, :w]
        mels_db = (mels_db - mels_db.min()) / (mels_db.max() - mels_db.min() + 1e-7)
        return np.reshape(mels_db, (1, h, w, 1))
def detect_audio_spoof(wav_path):
    try:
        pa_input = auto_prepare_audio(wav_path, pa_model.input_shape)
        la_input = auto_prepare_audio(wav_path, la_model.input_shape)
        
        pa_score = float(pa_model.predict(pa_input, verbose=0)[0][0])
        la_score = float(la_model.predict(la_input, verbose=0)[0][0])
        
        LA_THRESHOLD = 0.36  
        PA_THRESHOLD = 0.15  
        
        is_la_fake = la_score < LA_THRESHOLD
        is_pa_fake = pa_score >= PA_THRESHOLD
        
        real_confidence = la_score * 100
        fake_confidence = (1.0 - la_score) * 100
        
        if is_pa_fake and pa_score > (1.0 - la_score):
            fake_confidence = pa_score * 100
            real_confidence = (1.0 - pa_score) * 100

        if is_la_fake:
            if la_score >= 0.25:
                label = "Suspicious"
                details = "Highly Compressed/Noisy (Cannot verify 100% authenticity)"
            else:
                label = "Manipulated"
                details = "AI Generated / Deepfake"
                
        elif is_pa_fake:
            label = "Manipulated"
            details = "Replay Attack (Recorded Audio)"
            
        else:
            label = "Authentic"
            details = "Verified Clear Voice"

        return {
            "la_raw_score": la_score, 
            "pa_raw_score": pa_score,
            "overall_score": fake_confidence,       
            "real_confidence": real_confidence,     
            "label": label,                         
            "details": details
        }
        
    except Exception as e:
        print(f"Audio Processing Error: {e}")
        return None