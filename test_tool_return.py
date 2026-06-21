import os
from dotenv import load_dotenv
load_dotenv()
from execution.tools import get_community_reports

res = get_community_reports.invoke({
    "classification": "early blight",
    "zone": "Austin, Texas",
    "current_image_path": "test"
})

print("TYPE:", type(res))
print("VALUE:", res)
