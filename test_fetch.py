import os
import json
from dotenv import load_dotenv
load_dotenv()
from execution.tools import get_community_reports
from supabase import create_client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

classification = "Tomato (Solanum lycopersicum) - early blight (Alternaria solani)"
res = get_community_reports.invoke({
    "classification": classification,
    "zone": "Austin, Texas",
    "current_image_path": "test"
})
print("Result:", res)
