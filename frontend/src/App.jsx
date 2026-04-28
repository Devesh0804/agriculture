// src/App.jsx
import { useState } from "react";
import CropForm from "./components/CropForm";
import FertilizerForm from "./components/FertilizerForm";
import DiseaseUpload from "./components/DiseaseUpload";

export default function App() {
  const [tab, setTab] = useState("crop");

  return (
    <div className="container">
      <h1>🌾 Smart Agriculture AI</h1>
      <p className="subtitle">Crop recommendation, fertilizer advice & disease detection powered by ML</p>

      <div className="tabs">
        <button className={`tab ${tab === "crop" ? "active" : ""}`} onClick={() => setTab("crop")}>🌱 Crop</button>
        <button className={`tab ${tab === "fertilizer" ? "active" : ""}`} onClick={() => setTab("fertilizer")}>🧪 Fertilizer</button>
        <button className={`tab ${tab === "disease" ? "active" : ""}`} onClick={() => setTab("disease")}>🦠 Disease</button>
      </div>

      {tab === "crop" && <CropForm />}
      {tab === "fertilizer" && <FertilizerForm />}
      {tab === "disease" && <DiseaseUpload />}
    </div>
  );
}