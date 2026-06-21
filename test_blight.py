import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()
from orchestrator import run_ecosentinel_agent

# Download a real Tomato Early Blight image
url = "https://extension.umn.edu/sites/extension.umn.edu/files/styles/caption_medium/public/early-blight-tomato-leaf-2.jpg"
image_path = "real_tomato_early_blight.jpg"

try:
    print("Downloading test image of Tomato Early Blight...")
    with open(image_path, "wb") as f:
        f.write(requests.get(url).content)
        
    print("Running EcoSentinel Pipeline...")
    result = run_ecosentinel_agent(image_path, "Austin, Texas", "Test run before final submission")
    
    print("\n" + "="*50)
    print("🚀 PIPELINE SUCCESS! FINAL OUTPUT JSON:")
    print("="*50)
    print(json.dumps(result, indent=2))
    print("="*50)
    
except Exception as e:
    import traceback
    traceback.print_exc()
    print("PIPELINE ERROR:", str(e))
