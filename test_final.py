import os
import glob
from dotenv import load_dotenv
load_dotenv()
from orchestrator import run_ecosentinel_agent
from orchestrator import run_ecosentinel_agent
import json

# Find the most recently created .jpg file in the current directory
jpg_files = glob.glob("*.jpg")
if not jpg_files:
    print("NO JPG FILES FOUND!")
    # Download a test image
    import requests
    url = "https://raw.githubusercontent.com/pjreddie/darknet/master/data/dog.jpg"
    with open("test_image.jpg", "wb") as f:
        f.write(requests.get(url).content)
    test_image = "test_image.jpg"
else:
    # Sort by creation time
    test_image = max(jpg_files, key=os.path.getctime)

print(f"Using image: {test_image}")

try:
    result = run_ecosentinel_agent(test_image, "Austin, Texas", "Testing final submission pipeline")
    print(json.dumps(result, indent=2))
except Exception as e:
    import traceback
    traceback.print_exc()
    print("PIPELINE ERROR:", str(e))
