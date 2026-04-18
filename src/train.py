# 🔥 HIGH ACCURACY VERSION (UPDATE train.py)

import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torchvision.models import mobilenet_v2, MobileNet_V2_Weights
from torch.utils.data import DataLoader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAIN_DIR = os.path.join(BASE_DIR, "..", "data", "train")
VAL_DIR = os.path.join(BASE_DIR, "..", "data", "val")
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "disease_model.pt")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# =========================
# BETTER TRANSFORMS
# =========================
train_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(20),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
])

val_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

train_dataset = datasets.ImageFolder(TRAIN_DIR, transform=train_transform)
val_dataset = datasets.ImageFolder(VAL_DIR, transform=val_transform)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=0)
val_loader = DataLoader(val_dataset, batch_size=32, num_workers=0)

print(f"🔥 Train: {len(train_dataset)} | Val: {len(val_dataset)}")

# =========================
# MODEL (UNFREEZE FOR ACCURACY)
# =========================
model = mobilenet_v2(weights=MobileNet_V2_Weights.DEFAULT)

model.classifier[1] = nn.Linear(model.last_channel, len(train_dataset.classes))
model = model.to(device)

# =========================
# TRAIN SETUP
# =========================
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.0003)

EPOCHS = 5

# =========================
# TRAIN LOOP
# =========================
for epoch in range(EPOCHS):
    print(f"\n🚀 Epoch {epoch+1}/{EPOCHS}")
    model.train()
    correct = 0

    for i, (images, labels) in enumerate(train_loader):
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        _, preds = torch.max(outputs, 1)
        correct += (preds == labels).sum().item()

        if i % 20 == 0:
            print(f"Step {i}/{len(train_loader)}")

    train_acc = correct / len(train_dataset)

    # VALIDATION
    model.eval()
    correct = 0

    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, preds = torch.max(outputs, 1)
            correct += (preds == labels).sum().item()

    val_acc = correct / len(val_dataset)

    print(f"✅ Train Acc: {train_acc:.4f} | Val Acc: {val_acc:.4f}")


os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

torch.save({
    "model_state": model.state_dict(),
    "classes": train_dataset.classes
}, MODEL_PATH)

print("\n🏆 HIGH ACCURACY MODEL SAVED!")