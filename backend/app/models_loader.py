import joblib
import torch
import os
import torchvision.models as models

from .config import MODEL_DIR

# Global variables
crop_model = None
fert_type_model = None
fert_qty_model = None
disease_model = None
disease_classes = []
crop_encoder = None
fert_encoder = None
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Track loading errors
_load_errors: dict[str, str] = {}


def load_models():
    global crop_model, fert_type_model, fert_qty_model
    global disease_model, disease_classes
    global crop_encoder, fert_encoder

    # --- sklearn models ---
    try:
        crop_model = joblib.load(os.path.join(MODEL_DIR, "crop_model.pkl"))
        print("  ✔ crop_model loaded")
    except Exception as e:
        _load_errors["crop_model"] = str(e)
        print(f"  ✘ crop_model failed: {e}")

    try:
        fert_type_model = joblib.load(os.path.join(MODEL_DIR, "fertilizer_type_model.pkl"))
        print("  ✔ fert_type_model loaded")
    except Exception as e:
        _load_errors["fert_type_model"] = str(e)
        print(f"  ✘ fert_type_model failed: {e}")

    try:
        fert_qty_model = joblib.load(os.path.join(MODEL_DIR, "fertilizer_quantity_model.pkl"))
        print("  ✔ fert_qty_model loaded")
    except Exception as e:
        _load_errors["fert_qty_model"] = str(e)
        print(f"  ✘ fert_qty_model failed: {e}")

    # --- encoders ---
    try:
        crop_encoder = joblib.load(os.path.join(MODEL_DIR, "crop_encoder.pkl"))
        print("  ✔ crop_encoder loaded")
    except Exception as e:
        _load_errors["crop_encoder"] = str(e)
        print(f"  ✘ crop_encoder failed: {e}")

    try:
        fert_encoder = joblib.load(os.path.join(MODEL_DIR, "fertilizer_encoder.pkl"))
        print("  ✔ fert_encoder loaded")
    except Exception as e:
        _load_errors["fert_encoder"] = str(e)
        print(f"  ✘ fert_encoder failed: {e}")

    # --- disease DL model ---
    try:
        checkpoint = torch.load(
            os.path.join(MODEL_DIR, "disease_model.pt"),
            map_location=device,
        )

        if isinstance(checkpoint, dict) and "model_state" in checkpoint:
            disease_classes = checkpoint.get("classes", [])
            num_classes = len(disease_classes) or 4
            disease_model = models.mobilenet_v2(weights=None)
            disease_model.classifier[1] = torch.nn.Linear(
                disease_model.last_channel, num_classes
            )
            disease_model.load_state_dict(checkpoint["model_state"])

        elif isinstance(checkpoint, torch.nn.Module):
            disease_model = checkpoint
            disease_classes = []

        elif isinstance(checkpoint, dict):
            disease_model = models.mobilenet_v2(weights=None)
            disease_model.classifier[1] = torch.nn.Linear(
                disease_model.last_channel, 4
            )
            disease_model.load_state_dict(checkpoint)
            disease_classes = []

        else:
            raise ValueError("Unsupported checkpoint format")

        disease_model.to(device)
        disease_model.eval()
        print("  ✔ disease_model loaded")

    except Exception as e:
        _load_errors["disease_model"] = str(e)
        print(f"  ✘ disease_model failed: {e}")

    if _load_errors:
        print(f"\n⚠  {len(_load_errors)} model(s) failed to load — those endpoints will return 503")
    else:
        print("\n✅ All models and encoders loaded successfully!")


def get_status() -> dict:
    """Return a dict describing which models are available."""
    return {
        "crop_model": crop_model is not None,
        "fert_type_model": fert_type_model is not None,
        "fert_qty_model": fert_qty_model is not None,
        "crop_encoder": crop_encoder is not None,
        "fert_encoder": fert_encoder is not None,
        "disease_model": disease_model is not None,
        "errors": _load_errors,
    }