// src/components/DiseaseUpload.jsx

import { useState } from "react";
import { predictDisease } from "../api";

function DiseaseUpload() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    try {
      const res = await predictDisease(formData);
      setResult(res.data);
    } catch (err) {
      console.error(err);
      setResult(null);
    }
    setLoading(false);
  };

  return (
    <div className="card">
      <h2>Disease Detection</h2>

      <input type="file" onChange={(e) => setFile(e.target.files[0])} />

      <button onClick={handleSubmit}>
        {loading ? "Loading..." : "Upload"}
      </button>

      {result && (
        <div className="card">
          🍃 {result.disease} <br />
          Confidence: {result.confidence}%
        </div>
      )}
    </div>
  );
}

export default DiseaseUpload;