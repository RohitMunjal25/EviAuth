import subprocess
import os
import shutil
import time
from models.dfdcmodel import detect_deepfake
from models.faceforensics import detect_faceforensics
from exiftool import extract_metadata 

def extract_frames(video_path, output_folder="frames"):
    if os.path.exists(output_folder):
        try:
            shutil.rmtree(output_folder, ignore_errors=True)
        except:
            pass
            
    os.makedirs(output_folder, exist_ok=True)

    cmd = [
        "ffmpeg", "-i", video_path, 
        "-vf", "fps=5", 
        "-q:v", "2", 
        os.path.join(output_folder, "frame_%04d.jpg")
    ]
    
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    frames = sorted(os.listdir(output_folder))
    return len(frames), output_folder

def run_video_forensics(video_path):
    metadata = extract_metadata(video_path)
    
    frame_count, folder = extract_frames(video_path)
    
    if frame_count == 0:
        return {
            "error": "FFmpeg could not extract frames.",
            "metadata": metadata, 
            "frames_checked": 0
        }

    try:
        dfdc_result = detect_deepfake(folder)
        ff_result = detect_faceforensics(folder)
        time.sleep(1.5) 

        return {
            "dfdc": dfdc_result,
            "faceforensics": ff_result,
            "metadata": metadata, 
            "frames_checked": frame_count
        }

    except Exception as e:
        print(f"❌ Forensic Error: {e}")
        return {
            "error": str(e),
            "metadata": metadata, 
            "frames_checked": frame_count
        }
        
    finally:
        # 4. Final Cleanup
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)