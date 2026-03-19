import subprocess
import json
import os
import platform 
from PIL import Image
from PIL.ExifTags import TAGS

def extract_metadata(file_path):
    metadata = {}
    abs_path = os.path.normpath(os.path.abspath(file_path))
    ext = file_path.split('.')[-1].lower()

    try:
        if platform.system() == "Windows":
            current_dir = os.path.dirname(os.path.abspath(__file__))
            exiftool_path = os.path.join(current_dir, 'tools', 'exiftool.exe')
            cmd = f'"{exiftool_path}" -api LargeFileSupport=1 -j -G "{abs_path}"'
        else:
            cmd = f'exiftool -api LargeFileSupport=1 -j -G "{abs_path}"'
        
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        
        if result.stdout:
            data = json.loads(result.stdout)[0]
            metadata = {k.split(']')[-1]: v for k, v in data.items()}
            print(f" ExifTool Found ({platform.system()} Mode): {metadata.get('Model', 'Unknown')}")
            
    except Exception as e:
        print(f"ExifTool failed: {e}")

    if not metadata.get('Model') and ext in ['jpg', 'jpeg', 'png']:
        try:
            print("Falling back to Pillow for Image...")
            with Image.open(abs_path) as img:
                info = img._getexif()
                if info:
                    for tag, value in info.items():
                        decoded = TAGS.get(tag, tag)
                        metadata[decoded] = value
            print(f"Pillow Recovered: {metadata.get('Model', 'Unknown')}")
        except Exception as e:
            print(f" Pillow also failed: {e}")

    return metadata