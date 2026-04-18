# FIX: FASTER + SAFE SPLIT (WITH PROGRESS + SKIP EXISTING)

import os
import random
import shutil

BASE_DIR = "data"
TRAIN_DIR = os.path.join(BASE_DIR, "train")
VAL_DIR = os.path.join(BASE_DIR, "val")

SPLIT_RATIO = 0.2

os.makedirs(VAL_DIR, exist_ok=True)

for class_name in os.listdir(TRAIN_DIR):
    class_path = os.path.join(TRAIN_DIR, class_name)

    if not os.path.isdir(class_path):
        continue

    images = [img for img in os.listdir(class_path)
              if img.lower().endswith((".jpg", ".jpeg", ".png"))]

    if len(images) == 0:
        continue

    random.shuffle(images)
    split_count = int(len(images) * SPLIT_RATIO)

    val_class_path = os.path.join(VAL_DIR, class_name)
    os.makedirs(val_class_path, exist_ok=True)

    moved = 0

    for i, img in enumerate(images[:split_count]):
        src = os.path.join(class_path, img)
        dst = os.path.join(val_class_path, img)

        if not os.path.exists(dst) and os.path.exists(src):
            shutil.move(src, dst)
            moved += 1

        # progress print every 100 images
        if i % 100 == 0:
            print(f"{class_name}: {i}/{split_count} done")

    print(f"✅ {class_name} → moved {moved} images")

print("\n🔥 DONE: Dataset split completed!")