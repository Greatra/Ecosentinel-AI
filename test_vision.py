import os
import requests
from dotenv import load_dotenv
load_dotenv()
from execution.tools import analyze_image_vision

img_data = requests.get("https://raw.githubusercontent.com/pjreddie/darknet/master/data/dog.jpg").content
with open("dog.jpg", "wb") as f:
    f.write(img_data)

try:
    res = analyze_image_vision.invoke({
        "image_path": "dog.jpg",
        "context_notes": ""
    })
    print("SUCCESS")
    print(res)
except Exception as e:
    print("FAILED")
    print(e)
