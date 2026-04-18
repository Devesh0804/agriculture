from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from PIL import Image
import io
import torch
import torchvision.transforms as transforms
import os
import joblib

from app.schemas import (
    CropRequest,
    CropResponse,
    FertilizerRequest,
    FertilizerResponse,
    DiseaseResponse,
)

import app.models_loader as ml

app = FastAPI(title="Agri AI API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CROP_ENCODER_PATH = os.path.join(BASE_DIR, "models", "crop_encoder.pkl")
FERT_ENCODER_PATH = os.path.join(BASE_DIR, "models", "fertilizer_encoder.pkl")

# Load encoders
crop_encoder = joblib.load(CROP_ENCODER_PATH)
fert_encoder = joblib.load(FERT_ENCODER_PATH)

# ✅ YOUR ACTUAL DISEASE CLASSES (MATCH TRAINING ORDER)
disease_classes = [
    "Potato Early Blight",
    "Potato Late Blight",
    "Tomato Late Blight",
    "Tomato Healthy"
]

# Load models at startup
@app.on_event("startup")
def startup_event():
    ml.load_models()
    print("✅ Models loaded inside FastAPI")


# Root
@app.get("/")
def root():
    return {"message": "API is running"}


# ----------- CROP PREDICTION -----------
@app.post("/predict-crop", response_model=CropResponse)
def predict_crop(data: CropRequest):
    if ml.crop_model is None:
        raise HTTPException(status_code=500, detail="Crop model not loaded")

    try:
        features = np.array([
            data.N,
            data.P,
            data.K,
            data.temperature,
            data.humidity,
            data.ph,
            data.rainfall
        ]).reshape(1, -1)

        prediction = ml.crop_model.predict(features)[0]

        return {"crop": str(prediction)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------- FERTILIZER PREDICTION -----------
@app.post("/predict-fertilizer", response_model=FertilizerResponse)
def predict_fertilizer(data: FertilizerRequest):
    if ml.fert_type_model is None or ml.fert_qty_model is None:
        raise HTTPException(status_code=500, detail="Fertilizer models not loaded")

    try:
        # Match training preprocessing
        crop_input = data.crop.strip().lower()

        if crop_input not in crop_encoder.classes_:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid crop. Allowed: {list(crop_encoder.classes_)}"
            )

        crop_encoded = crop_encoder.transform([crop_input])[0]

        # Feature order must match training
        features = np.array([
            data.N,
            data.P,
            data.K,
            data.ph,
            data.temperature,
            data.humidity,
            data.rainfall,
            crop_encoded
        ]).reshape(1, -1)

        fert_encoded = ml.fert_type_model.predict(features)[0]
        fertilizer = fert_encoder.inverse_transform([fert_encoded])[0]

        quantity = ml.fert_qty_model.predict(features)[0]

        return {
            "fertilizer_type": str(fertilizer),
            "quantity": float(quantity)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------- DISEASE PREDICTION -----------
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])


@app.post("/predict-disease", response_model=DiseaseResponse)
async def predict_disease(file: UploadFile = File(...)):
    if ml.disease_model is None:
        raise HTTPException(status_code=500, detail="Disease model not loaded")

    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        img = transform(image).unsqueeze(0).to(ml.device)

        with torch.no_grad():
            outputs = ml.disease_model(img)
            probs = torch.nn.functional.softmax(outputs[0], dim=0)

            confidence, predicted = torch.max(probs, 0)

        pred_idx = predicted.item()
        disease_name = disease_classes[pred_idx] if pred_idx < len(disease_classes) else "Unknown"

        return {
            "disease": disease_name,
            "confidence": round(float(confidence.item()) * 100, 2)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))