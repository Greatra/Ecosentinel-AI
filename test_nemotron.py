import os
import glob
from dotenv import load_dotenv
load_dotenv()
from execution.tools import analyze_image_vision

print("Testing Vision Analysis with Nemotron Omni...")
# Create a dummy image
from PIL import Image
Image.new('RGB', (100, 100), color = 'red').save('test_image_nemotron.jpg')

try:
    result = analyze_image_vision.invoke({
        "image_path": "test_image_nemotron.jpg",
        "context_notes": "Test"
    })
    print("SUCCESS!")
    print(result)
except Exception as e:
    import traceback
    traceback.print_exc()
    print("VISION ERROR:", str(e))
