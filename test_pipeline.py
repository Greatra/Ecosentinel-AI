import os
import json
from dotenv import load_dotenv

# Load env before importing anything
load_dotenv()

from orchestrator import run_ecosentinel_agent

def main():
    print("Testing pipeline directly...")
    image_path = r"D:\USA GLOBAL HACKATHON\demo dataset\concrete rings close up(tomato early bright).jpg"
    zone = "Austin, Texas"
    notes = "Testing the system to ensure no error loops occur."
    
    try:
        final_state = run_ecosentinel_agent(image_path, zone, notes)
        print("\n\n=== PIPELINE SUCCESS ===")
        print(json.dumps(final_state, indent=2))
    except Exception as e:
        print(f"\n\n=== PIPELINE FATAL CRASH ===")
        print(str(e))
        import sys
        sys.exit(1)

if __name__ == "__main__":
    main()
