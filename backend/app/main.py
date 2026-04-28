from contextlib import asynccontextmanager
import os

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import numpy as np
from PIL import Image
import io
import torch
import torchvision.transforms as transforms

from .schemas import (
    CropRequest,
    CropResponse,
    FertilizerRequest,
    FertilizerResponse,
    DiseaseResponse,
)
from .config import CORS_ORIGINS, BASE_DIR
from . import models_loader as ml


# -----------  LIFESPAN  -----------
@asynccontextmanager
async def lifespan(app: FastAPI):
    ml.load_models()
    print("Models loaded — API is ready")
    yield


app = FastAPI(title="Agri AI API", lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------  ROOT  -----------
@app.get("/")
def root():
    return {"message": "Agri AI API is running"}


# -----------  HEALTH CHECK  -----------
@app.get("/api/health")
def health():
    status = ml.get_status()
    all_ok = all(v for k, v in status.items() if k != "errors")
    return {
        "status": "ok" if all_ok else "degraded",
        "models": status,
    }


# -----------  CROP PREDICTION  -----------
@app.post("/api/predict-crop", response_model=CropResponse)
def predict_crop(data: CropRequest):
    if ml.crop_model is None:
        raise HTTPException(status_code=503, detail="Crop model not loaded")

    try:
        features = np.array([
            data.N, data.P, data.K,
            data.temperature, data.humidity,
            data.ph, data.rainfall,
        ]).reshape(1, -1)

        prediction = ml.crop_model.predict(features)[0]
        return {"crop": str(prediction)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")


# -----------  FERTILIZER PREDICTION  -----------
@app.post("/api/predict-fertilizer", response_model=FertilizerResponse)
def predict_fertilizer(data: FertilizerRequest):
    if ml.fert_type_model is None or ml.fert_qty_model is None:
        raise HTTPException(status_code=503, detail="Fertilizer models not loaded")

    if ml.crop_encoder is None or ml.fert_encoder is None:
        raise HTTPException(status_code=503, detail="Encoders not loaded")

    try:
        crop_input = data.crop.strip().lower()

        if crop_input not in ml.crop_encoder.classes_:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown crop '{crop_input}'. Allowed: {list(ml.crop_encoder.classes_)}",
            )

        crop_encoded = ml.crop_encoder.transform([crop_input])[0]

        features = np.array([
            data.N, data.P, data.K,
            data.ph, data.temperature,
            data.humidity, data.rainfall,
            crop_encoded,
        ]).reshape(1, -1)

        fert_encoded = ml.fert_type_model.predict(features)[0]
        fertilizer = ml.fert_encoder.inverse_transform([fert_encoded])[0]
        quantity = ml.fert_qty_model.predict(features)[0]

        return {
            "fertilizer_type": str(fertilizer),
            "quantity": float(quantity),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")


# -----------  DISEASE PREDICTION  -----------
_disease_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])


@app.post("/api/predict-disease", response_model=DiseaseResponse)
async def predict_disease(file: UploadFile = File(...)):
    if ml.disease_model is None:
        raise HTTPException(status_code=503, detail="Disease model not loaded")

    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img = _disease_transform(image).unsqueeze(0).to(ml.device)

        with torch.no_grad():
            outputs = ml.disease_model(img)
            probs = torch.nn.functional.softmax(outputs[0], dim=0)
            confidence, predicted = torch.max(probs, 0)

        pred_idx = predicted.item()

        # Use classes from checkpoint (loaded dynamically)
        if ml.disease_classes and pred_idx < len(ml.disease_classes):
            disease_name = ml.disease_classes[pred_idx]
        else:
            disease_name = f"Class {pred_idx}"

        return {
            "disease": disease_name,
            "confidence": round(float(confidence.item()) * 100, 2),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")


# -----------  STATIC FILES (production)  -----------
_frontend_dist = os.path.join(BASE_DIR, "frontend", "dist")

if os.path.isdir(_frontend_dist):
    # Serve built assets (JS, CSS, images)
    app.mount("/assets", StaticFiles(directory=os.path.join(_frontend_dist, "assets")), name="assets")

    # SPA catch-all: serve index.html for any non-API route
    @app.get("/{path:path}")
    async def serve_spa(path: str):
        file_path = os.path.join(_frontend_dist, path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(_frontend_dist, "index.html"))

