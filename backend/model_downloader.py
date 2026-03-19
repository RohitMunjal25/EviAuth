import os
import requests
try:
    from tqdm import tqdm
except ImportError:
    print("'tqdm' module not found. Run: pip install tqdm")
    exit()

HF_BASE_URL = "https://huggingface.co/RohitMunjal/rohitbackendmodels/resolve/main/"

MODELS_TO_DOWNLOAD = {
    "asvspoof_la_model.h5": f"{HF_BASE_URL}asvspoof_la_model.h5",
    "asvspoof_pa_model.h5": f"{HF_BASE_URL}asvspoof_pa_model.h5",
    "midv500.keras": f"{HF_BASE_URL}midv500.keras",
    "casia_model.h5": f"{HF_BASE_URL}casia_model.h5",
    "dfdc_model.h5": f"{HF_BASE_URL}dfdc_model.h5",
    "faceforensics_model.h5": f"{HF_BASE_URL}faceforensics_model.h5",
    "cifake.keras": f"{HF_BASE_URL}cifake.keras"
}

MODELS_DIR = "models"

def download_file(url, filepath):
    """File ko stream karke download karega with Progress Bar"""
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024 * 1024 

    print(f" Downloading: {os.path.basename(filepath)}")
    with open(filepath, 'wb') as file, tqdm(
        total=total_size, unit='iB', unit_scale=True, desc=os.path.basename(filepath)
    ) as progress_bar:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)

def ensure_models_exist():
    print("Checking AI Models status...")
    
    if not os.path.exists(MODELS_DIR):
        print(f"'{MODELS_DIR}' folder not found. Creating it...")
        os.makedirs(MODELS_DIR)

    all_downloaded = True
    
    for model_name, url in MODELS_TO_DOWNLOAD.items():
        model_path = os.path.join(MODELS_DIR, model_name)
        
        if not os.path.exists(model_path):
            all_downloaded = False
            try:
                download_file(url, model_path)
                print(f" {model_name} downloaded successfully!\n")
            except Exception as e:
                print(f" Failed to download {model_name}. Error: {e}\n")
                
    if all_downloaded:
        print("All AI models are already present and ready to roll!\n")

if __name__ == "__main__":
    ensure_models_exist()