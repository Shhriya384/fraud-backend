from flask import Flask, request, jsonify
from supabase import create_client, Client
import numpy as np
import pickle
import tensorflow as tf
from datetime import datetime
import traceback

# ✅ Initialize Flask app
app = Flask(__name__)

# ✅ Supabase connection
url = "https://qbdoojkpbgmkmgchjotg.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFiZG9vamtwYmdta21nY2hqb3RnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE2OTY0MjgsImV4cCI6MjA2NzI3MjQyOH0.8y2zMgtpBpFN5fP4Cz8yjVfnbIZOfJ5JXg6oVjvEuEg"
supabase: Client = create_client(url, key)

# ✅ Load Autoencoder model and scaler
try:
    model = tf.keras.models.load_model("autoencoder_model.keras")
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    print("✅ Model and scaler loaded successfully.")
except Exception as load_error:
    print("❌ Error loading model or scaler:", load_error)
    exit()

# ✅ Prediction API
@app.route("/predict", methods=["POST"])
def predict():
    try:
        if not request.is_json:
            raise ValueError("Request content-type must be application/json")

        data = request.json
        print("📥 Raw request JSON:", data)

        features = data.get("features")
        if features is None:
            raise ValueError("Missing 'features' in JSON payload")

        if len(features) != 30:
            raise ValueError("Exactly 30 features required (Time, V1–V28, Amount)")

        # Scale input
        features_scaled = scaler.transform([features])
        print("🔢 Scaled features:", features_scaled)

        # Predict using Autoencoder
        reconstructed = model.predict(features_scaled, verbose=0)
        error = np.mean((features_scaled - reconstructed) ** 2)

        # Set fraud threshold
        threshold = 0.0001
        result = "FRAUDULENT" if error > threshold else "SAFE"
        print(f"🔍 Prediction: {result} | Error: {error}")

        # Insert result to Supabase
        supabase.table("transactions").insert({
            "time": features[0],
            "amount": features[29],
            "prediction": result,
            "timestamp": datetime.utcnow().isoformat()
        }).execute()

        # Return result
        return jsonify({
            "prediction": result,
            "reconstruction_error": error
        })

    except Exception as e:
        print("❌ INTERNAL ERROR:", str(e))
        traceback.print_exc()
        return jsonify({"error": str(e)}), 400

# ✅ Run server
if __name__ == "__main__":
    app.run(debug=True)
