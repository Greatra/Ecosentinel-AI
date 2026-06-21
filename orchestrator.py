import os
import json
import re
from execution.tools import (
    analyze_image_vision,
    get_weather_data,
    generate_treatment_recommendation,
    safety_review_nemotron,
    generate_executive_summary_nemotron
)
from supabase import create_client, Client

def run_ecosentinel_agent(image_path: str, location_name: str, notes: str = "") -> dict:
    """Orchestrates the entire EcoSentinel pipeline deterministically."""
    
    # 1. Call vision
    vision_result_str = analyze_image_vision.invoke({
        "image_path": image_path,
        "context_notes": notes
    })
        
    content = vision_result_str.replace("Vision Analysis Result:\n", "").strip()
    try:
        vision_data = json.loads(content)
    except json.JSONDecodeError:
        raise Exception("CASCADE_HALT: Vision model failed to return valid JSON.")
        
    classification = vision_data.get("classification", "Unknown")
    confidence = float(vision_data.get("confidence", 0.0))
    
    # 2. Check confidence > 0.70 or raise Exception
    if confidence < 0.70:
        evidence = vision_data.get("evidence_summary", "Confidence below threshold.")
        raise Exception(f"CASCADE_HALT: Confidence {confidence} is below 0.70 threshold. {evidence}")
        
    # 3. Call weather
    weather_result = get_weather_data.invoke({"location_name": location_name})
    
    
    def extract_json(text: str, required_keys: list = None) -> dict:
        import re
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1 and end >= start:
            json_str = text[start:end+1]
        else:
            json_str = text
            
        try:
            parsed = json.loads(json_str)
            if required_keys:
                missing = [k for k in required_keys if k not in parsed]
                if missing:
                    raise Exception(f"JSON missing required keys: {missing}")
            return parsed
        except json.JSONDecodeError as e:
            # Raise a hard exception so the pipeline halts immediately per Nightmare Protocol
            raise Exception(f"CASCADE_HALT: Failed to parse JSON response. Error: {e}\nRaw output: {text}") from e
        except Exception as e:
            raise Exception(f"CASCADE_HALT: JSON Schema Validation Failed. {e}\nRaw output: {text}") from e

    # 4. Generate Treatment Recommendations
    recommendation_str = generate_treatment_recommendation.invoke({
        "vision_data": vision_result_str,
        "weather_data": weather_result,
        "community_data": "None available"
    })
    recommendation_dict = extract_json(recommendation_str, required_keys=["immediate_actions", "preventive_measures"])
    
    # 6. Call safety
    safety_str = safety_review_nemotron.invoke({"recommendations": recommendation_str})
    safety_dict = extract_json(safety_str, required_keys=["status", "pollinator_risk", "human_oversight"])
    
    # 7. Call summary
    state_summary = (
        f"Vision:\n{vision_result_str}\n\n"
        f"Weather:\n{weather_result}\n\n"
        f"Recommendations:\n{recommendation_str}\n\n"
        f"Safety:\n{safety_str}"
    )
    summary_str = generate_executive_summary_nemotron.invoke({"state_summary": state_summary})
    summary_dict = extract_json(summary_str, required_keys=["current_situation"])
    
    # Construct final dictionary
    temp = "Unavailable"
    humidity = "Unavailable"
    wind = "Unavailable"
    
    temp_match = re.search(r"Temperature ([\d\.\-]+)°C", weather_result)
    if temp_match: temp = temp_match.group(1)
    
    hum_match = re.search(r"Humidity ([\d\.\-]+)%", weather_result)
    if hum_match: humidity = hum_match.group(1)
    
    wind_match = re.search(r"Wind ([\d\.\-]+)", weather_result)
    if wind_match: wind = wind_match.group(1)
    
    risk_level = "MODERATE"
    risk_reason = f"Current temperature ({temp}°C) and humidity ({humidity}%) are within typical ranges, requiring only standard monitoring."
    
    # ECC Layer 3: Deterministic Logic Gate using Weather Data
    try:
        temp_val = float(temp)
        hum_val = float(humidity)
        
        if hum_val > 80.0 and temp_val > 25.0:
            risk_level = "HIGH"
            risk_reason = f"High humidity ({hum_val}%) and warm temperatures ({temp_val}°C) create optimal conditions for rapid pathogen spread."
        elif hum_val > 75.0 or temp_val > 30.0:
            risk_level = "ELEVATED"
            risk_reason = "Current weather conditions mildly favor disease progression."
        elif hum_val < 50.0:
            risk_level = "LOW"
            risk_reason = "Low humidity environment significantly reduces the risk of rapid fungal spread."
    except ValueError as ve:
        print(f"Weather parsing failed, falling back to default MODERATE risk. Error: {ve}")

    vis_ev = vision_data.get("visible_evidence", [])
    unc = vision_data.get("uncertainty", [])
        
    data = {
        "classification": classification,
        "confidence": confidence,
        "visible_evidence": vis_ev,
        "uncertainty": unc,
        "temperature": temp,
        "humidity": humidity,
        "wind": wind,
        "risk_level": risk_level,
        "risk_reason": risk_reason,
        "treatment_actions": recommendation_dict,
        "safety_status": safety_dict,
        "summary_current_situation": summary_dict
    }
    
    # Supabase Insert
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        raise EnvironmentError("Missing Supabase credentials in .env")
        
    supabase: Client = create_client(url, key)
    
    classification_val = str(data.get("classification", "Unknown"))
    conf_val = float(data.get("confidence", 0.0))
    conf_val = max(0.0, min(1.0, conf_val))
    risk_val = str(data.get("risk_level", "MODERATE")).upper()
    
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"CASCADE_HALT: Target image path not found: {image_path}")

    insert_payload = {
        "pest_classification": classification_val[:255],
        "confidence_score": conf_val,
        "risk_level": risk_val,
        "zone": str(location_name)[:255],
        "image_url": f"local_observation:{os.path.basename(image_path)}"
    }
    
    supabase.table("reports").insert(insert_payload).execute()
        
    return data
