import joblib
import numpy as np

# =========================
# LOAD MODELS
# =========================
crop_model = joblib.load("models/crop_model.pkl")
fert_model = joblib.load("models/fertilizer_type_model.pkl")
qty_model = joblib.load("models/fertilizer_quantity_model.pkl")

# Load encoders
crop_encoder = joblib.load("models/crop_encoder.pkl")
fert_encoder = joblib.load("models/fertilizer_encoder.pkl")


# =========================
# INPUT (same as Phase 1)
# =========================
# order: N, P, K, temperature, humidity, ph, rainfall
input_data = np.array([[90, 42, 43, 20.8, 82, 6.5, 200]])


# =========================
# STEP 1: CROP PREDICTION
# =========================
crop_prediction = crop_model.predict(input_data)[0]

print("🌱 Recommended Crop:", crop_prediction)


# =========================
# STEP 2: ENCODE CROP
# =========================
crop_encoded = crop_encoder.transform([crop_prediction])[0]


# =========================
# STEP 3: FERTILIZER TYPE
# =========================
fert_input = np.array([[
    input_data[0][0],  # N
    input_data[0][1],  # P
    input_data[0][2],  # K
    input_data[0][5],  # pH
    input_data[0][3],  # temperature
    input_data[0][4],  # humidity
    input_data[0][6],  # rainfall
    crop_encoded
]])

fert_prediction = fert_model.predict(fert_input)[0]
fert_name = fert_encoder.inverse_transform([fert_prediction])[0]

print("🧪 Recommended Fertilizer:", fert_name)


# =========================
# STEP 4: QUANTITY
# =========================
quantity = qty_model.predict(fert_input)[0]

print("📦 Quantity (kg/hectare):", round(quantity, 2))