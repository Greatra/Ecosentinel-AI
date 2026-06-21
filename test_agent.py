import os
from orchestrator import run_ecosentinel_agent
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    # Create a dummy image
    dummy_image = "dummy.jpg"
    with open(dummy_image, "wb") as f:
        f.write(b"dummy")
    
    try:
        print("Running agent...")
        res = run_ecosentinel_agent(dummy_image, "North Garden")
        print("RESULT:")
        print(res)
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if os.path.exists(dummy_image):
            os.remove(dummy_image)
