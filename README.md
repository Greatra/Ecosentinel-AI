# EcoSentinel AI crop disease detection and weather insights

This system runs agricultural image analysis against local weather APIs to diagnose crop diseases. You pass an image of a leaf, and the script identifies the pathogen, checks current regional weather conditions, and returns direct treatment steps.

## Architecture overview

The application splits into two functional blocks. 

The orchestrator script (`orchestrator.py`) handles the primary agent loop. It intercepts user inputs, coordinates tool execution, and generates the final response. 

The tool execution module (`execution/tools.py`) connects to external APIs. It queries the Nvidia Nemotron vision model for image parsing and external weather APIs to pull location-specific humidity and temperature data.

Here is how it actually works: You provide an image path. The vision model isolates physical symptoms. The orchestrator then requests local weather data to verify if the environmental conditions match the suspected disease profile. The system outputs a structured diagnosis.

## Prerequisites

You need the following installed before running the code:
* Python 3.10 or higher.
* An active Supabase database (for storing community reports).
* API keys for Nvidia AI endpoints and your selected weather provider.

## Step-by-step setup commands

Suppose you have your terminal open to the repository root. Run these exact commands to build the environment.

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the root directory. Add your specific API keys.

```text
NVIDIA_API_KEY="your_nvidia_key"
WEATHER_API_KEY="your_weather_key"
SUPABASE_URL="your_supabase_url"
SUPABASE_KEY="your_supabase_key"
```

## Sample usage

When the environment is configured, start the main application loop.

```bash
python app.py
```

The terminal prompts you for an input. Type your query and include the absolute or relative path to your image file.

```text
User: Check this tomato leaf for early blight. The image is at assets/real_tomato_early_blight.jpg.
```

The system processes the file, retrieves the weather data, and prints the treatment logic to the console.
