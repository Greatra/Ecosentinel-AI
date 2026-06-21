from dotenv import load_dotenv
load_dotenv(override=True)

from orchestrator import run_ecosentinel_agent
import json
import os

print("NVIDIA API KEY:", os.environ.get("NVIDIA_API_KEY")[:10] + "...")
print("GEMINI API KEY:", os.environ.get("GEMINI_API_KEY")[:10] + "...")

try:
    result = run_ecosentinel_agent("temp_upload_04f6da372e7347739567d4f859807af6.jpg", "North Garden")
    print(json.dumps(result, indent=2))
except Exception as e:
    import traceback
    traceback.print_exc()
    print("PIPELINE ERROR:", str(e))
