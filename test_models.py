import os
import time
from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.messages import HumanMessage

load_dotenv(override=True)
api_key = os.environ.get("NVIDIA_API_KEY")

models = [
    {"name": "nemotron-nano", "model": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning", "kwargs": {"reasoning_budget": 2048, "max_tokens": 4096}},
    {"name": "nemotron-super", "model": "nvidia/nemotron-3-super-120b-a12b", "kwargs": {"max_tokens": 512}},
    {"name": "llama", "model": "meta/llama-3.1-70b-instruct", "kwargs": {"max_tokens": 512}},
    {"name": "glm", "model": "z-ai/glm-5.1", "kwargs": {"max_tokens": 512}}
]

print("Testing models...")
for m in models:
    print(f"\n--- Testing {m['name']} ({m['model']}) ---")
    try:
        start_time = time.time()
        client = ChatNVIDIA(model=m["model"], api_key=api_key, **m["kwargs"])
        response = client.invoke([HumanMessage(content="Hello, respond with exactly one word: 'Alive'.")])
        elapsed = time.time() - start_time
        print(f"SUCCESS in {elapsed:.2f}s! Response: {response.content}")
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"FAILED after {elapsed:.2f}s! Error: {e}")
