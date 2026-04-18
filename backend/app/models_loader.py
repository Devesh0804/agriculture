import joblib
import torch
import os
import torchvision.models as models

# backend/app/models_loader.py → go 2 levels up → AGRICULTURE → models/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, "models")

# Global variables
crop_model = None
fert_type_model = None
fert_qty_model = None
disease_model = None
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def load_models():
    global crop_model, fert_type_model, fert_qty_model, disease_model

    # ✅ Load ML models
    crop_model = joblib.load(os.path.join(MODEL_PATH, "crop_model.pkl"))
    fert_type_model = joblib.load(os.path.join(MODEL_PATH, "fertilizer_type_model.pkl"))
    fert_qty_model = joblib.load(os.path.join(MODEL_PATH, "fertilizer_quantity_model.pkl"))

    # ✅ Load DL model
    checkpoint = torch.load(
        os.path.join(MODEL_PATH, "disease_model.pt"),
        map_location=device
    )

    # =========================
    # HANDLE ALL CASES PROPERLY
    # =========================

    # 🔥 CASE 1: Your current format (CORRECT ONE)
    if isinstance(checkpoint, dict) and "model_state" in checkpoint:
        disease_model = models.mobilenet_v2(pretrained=False)

        num_classes = len(checkpoint.get("classes", [])) or 38

        disease_model.classifier[1] = torch.nn.Linear(
            disease_model.last_channel,
            num_classes
        )

        disease_model.load_state_dict(checkpoint["model_state"])

    # 🔥 CASE 2: Full model saved directly
    elif isinstance(checkpoint, torch.nn.Module):
        disease_model = checkpoint

    # 🔥 CASE 3: Only state_dict saved
    elif isinstance(checkpoint, dict):
        disease_model = models.mobilenet_v2(pretrained=False)

        disease_model.classifier[1] = torch.nn.Linear(
            disease_model.last_channel,
            38  # fallback
        )

        disease_model.load_state_dict(checkpoint)

    else:
        raise ValueError("Unsupported checkpoint format")

    # ✅ Final setup
    disease_model.to(device)
    disease_model.eval()

    print("✅ All models loaded successfully!")