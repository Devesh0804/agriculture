# FIX PATH + AUTO CHECK + CLEAR ERROR

import os
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image

# =========================
# PATH FIX (ABSOLUTE)
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "disease_model.pt")
IMAGE_PATH = os.path.join(BASE_DIR, "..", "data", "test.jpg")  # change if needed

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# =========================
# CHECK MODEL EXISTS
# =========================
if not os.path.exists(MODEL_PATH):
    print("❌ Model not found!")
    print("👉 First run: python src/train.py")
    exit()

# =========================
# LOAD MODEL
# =========================
checkpoint = torch.load(MODEL_PATH, map_location=device)
classes = checkpoint["classes"]

model = models.mobilenet_v2(pretrained=False)
model.classifier[1] = nn.Linear(model.last_channel, len(classes))
model.load_state_dict(checkpoint["model_state"])

model = model.to(device)
model.eval()

# =========================
# TRANSFORM
# =========================
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# =========================
# CHECK IMAGE
# =========================
if not os.path.exists(IMAGE_PATH):
    print("❌ Image not found! Put test.jpg in /data folder")
    exit()

# =========================
# LOAD IMAGE
# =========================
image = Image.open(IMAGE_PATH).convert("RGB")
image = transform(image).unsqueeze(0).to(device)

# =========================
# PREDICT
# =========================
with torch.no_grad():
    outputs = model(image)
    probs = torch.softmax(outputs, dim=1)
    confidence, pred = torch.max(probs, 1)

print("🦠 Disease:", classes[pred.item()])
print(f"📊 Confidence: {confidence.item()*100:.2f}%")