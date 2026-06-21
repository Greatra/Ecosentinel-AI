import requests
location_name = "Austin, Texas"
geocode_url = "https://geocoding-api.open-meteo.com/v1/search"
geo_resp = requests.get(geocode_url, params={"name": location_name, "count": 1, "format": "json"}, timeout=5)
print(geo_resp.json())
