// src/App.jsx
import { useState } from "react";
import CropForm from "./components/CropForm";
import FertilizerForm from "./components/FertilizerForm";
import DiseaseUpload from "./components/DiseaseUpload";

export default function App() {
  const [tab, setTab] = useState("crop");

  return (
    <div className="container">
      <h1>🌾 Smart Agriculture</h1>

      <div className="tabs">
        <div className={`tab ${tab === "crop" && "active"}`} onClick={() => setTab("crop")}>Crop</div>
        <div className={`tab ${tab === "fertilizer" && "active"}`} onClick={() => setTab("fertilizer")}>Fertilizer</div>
        <div className={`tab ${tab === "disease" && "active"}`} onClick={() => setTab("disease")}>Disease</div>
      </div>

      {tab === "crop" && <CropForm />}
      {tab === "fertilizer" && <FertilizerForm />}
      {tab === "disease" && <DiseaseUpload />}
    </div>
  );
}