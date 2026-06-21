import os
from dotenv import load_dotenv
load_dotenv()
from execution.tools import analyze_image_vision
import requests

# Download real blight image
url = "https://extension.umn.edu/sites/extension.umn.edu/files/styles/caption_medium/public/early-blight-tomato-leaf-2.jpg"
image_path = "real_tomato_early_blight.jpg"

print("Downloading test image...")
with open(image_path, "wb") as f:
    f.write(requests.get(url).content)

print("Running vision analysis...")
try:
    result = analyze_image_vision.invoke({
        "image_path": image_path,
        "context_notes": "Test"
    })
    print("SUCCESS!")
    print(result)
except Exception as e:
    import traceback
    traceback.print_exc()
    print("VISION ERROR:", str(e))
