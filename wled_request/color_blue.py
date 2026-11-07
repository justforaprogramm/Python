import requests
import json

wled_ip = "192.168.2.125"

url = f"http://{wled_ip}/json/state"

payload = {
    "on": True,
    "bri": 255,
    "seg": [
        {
            "col": [[0, 0, 255]]  # Blue
        }
    ]
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    print("✅ Farbe erfolgreich auf Blau gesetzt!")
else:
    print(f"❌ Fehler: {response.status_code} - {response.text}")