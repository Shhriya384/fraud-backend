
import requests

url = "http://127.0.0.1:5000/predict"

# ✅ Sample input: 30 values from your dataset format (Time, V1–V28, Amount)
sample_features = [
    100000.0, -1.359807, -0.072781, 2.536346, 1.378155, -0.338321,
    0.462388, 0.239599, 0.098698, 0.363787, 0.090794, -0.5516,
    -0.617801, -0.99139, -0.311169, 1.468177, -0.470401, 0.207971,
    0.025791, 0.403993, 0.251412, -0.018307, 0.277838, -0.110474,
    0.066928, 0.128539, -0.189115, 0.133558, 0.024309, 149.62
]

try:
    response = requests.post(url, json={"features": sample_features})
    response.raise_for_status()
    print("✅ Prediction response:", response.json())
except requests.exceptions.RequestException as err:
    print("❌ API request failed:", err)
    if err.response is not None:
        print("🔴 Response content:", err.response.text)

import requests

url = "http://127.0.0.1:5000/predict"

# ✅ Sample input: 30 values from your dataset format (Time, V1–V28, Amount)
sample_features = [
    100000.0, -1.359807, -0.072781, 2.536346, 1.378155, -0.338321,
    0.462388, 0.239599, 0.098698, 0.363787, 0.090794, -0.5516,
    -0.617801, -0.99139, -0.311169, 1.468177, -0.470401, 0.207971,
    0.025791, 0.403993, 0.251412, -0.018307, 0.277838, -0.110474,
    0.066928, 0.128539, -0.189115, 0.133558, 0.024309, 149.62
]

try:
    response = requests.post(url, json={"features": sample_features})
    response.raise_for_status()
    print("✅ Prediction response:", response.json())
except requests.exceptions.RequestException as err:
    print("❌ API request failed:", err)
    if err.response is not None:
        print("🔴 Response content:", err.response.text)

