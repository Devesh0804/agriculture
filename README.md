# 🌾 Smart Agriculture AI

AI-powered crop recommendation, fertilizer advice, and plant disease detection.

## Features

| Feature | Model | Input |
|---|---|---|
| Crop Recommendation | RandomForest Classifier | N, P, K, temperature, humidity, pH, rainfall |
| Fertilizer Advice | RandomForest Classifier + Regressor | Same + crop name |
| Disease Detection | MobileNetV2 (transfer learning) | Leaf image (JPG/PNG) |

## Tech Stack

- **Backend:** FastAPI + Uvicorn
- **Frontend:** React 19 + Vite
- **ML:** scikit-learn, PyTorch, torchvision

---

## Quick Start (Local)

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Install frontend dependencies

```bash
cd frontend
npm install
cd ..
```

### 3. Start the backend

```bash
uvicorn backend.app.main:app --reload --port 8000
```

### 4. Start the frontend (dev)

```bash
cd frontend
npm run dev
```

Open **http://localhost:5173** — the Vite dev proxy forwards API calls to the backend.

---

## Production Build

### Option A: Manual

```bash
# Build frontend
cd frontend && npm run build && cd ..

# Run backend (serves API + built frontend)
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

### Option B: Docker

```bash
docker compose up --build
```

Open **http://localhost:8000**

---

## Project Structure

```
agriculture/
├── backend/app/          # FastAPI API server
│   ├── main.py           # Routes + static serving
│   ├── schemas.py        # Pydantic models
│   ├── models_loader.py  # ML model loading
│   └── config.py         # Environment config
├── frontend/src/         # React UI
│   ├── components/       # CropForm, FertilizerForm, DiseaseUpload
│   └── api.js            # Axios API client
├── src/                  # ML training scripts
├── data/                 # Datasets (CSV + images)
├── models/               # Trained model files (.pkl, .pt)
├── Dockerfile            # Multi-stage build
└── docker-compose.yml    # One-command deploy
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `MODEL_DIR` | `./models` | Path to trained model files |
| `CORS_ORIGINS` | `http://localhost:5173` | Comma-separated allowed origins |
