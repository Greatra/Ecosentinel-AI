import os
from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.messages import HumanMessage

load_dotenv(override=True)

models_to_test = [
    {
        "name": "Llama 3.1 70B (Treatment)",
        "model": "meta/llama-3.1-70b-instruct",
        "key": os.environ.get("NVIDIA_LLAMA_KEY", "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")
    },
    {
        "name": "Nemotron (Safety)",
        "model": "nvidia/llama-3.3-nemotron-super-49b-v1",
        "key": os.environ.get("NVIDIA_NEMOTRON_KEY", "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")
    },
    {
        "name": "Qwen (Summary)",
        "model": "qwen/qwen3.5-397b-a17b",
        "key": os.environ.get("NVIDIA_QWEN_KEY", "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")
    }
]

for m in models_to_test:
    print(f"Testing {m['name']}...")
    try:
        client = ChatNVIDIA(
            model=m["model"],
            api_key=m["key"],
            temperature=0.1
        )
        res = client.invoke([HumanMessage(content="Hello! Please reply 'OK'.")])
        print(f"SUCCESS {m['name']}: {res.content}")
    except Exception as e:
        print(f"FAILED {m['name']}: {type(e).__name__} - {e}")
