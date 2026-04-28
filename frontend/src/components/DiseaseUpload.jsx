// src/components/DiseaseUpload.jsx
import { useState } from "react";
import { predictDisease } from "../api";

export default function DiseaseUpload() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected) {
      setFile(selected);
      setPreview(URL.createObjectURL(selected));
      setResult(null);
      setError("");
    }
  };

  const handleSubmit = async () => {
    if (!file) {
      setError("Please select an image first");
      return;
    }

    setError("");
    setResult(null);
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await predictDisease(formData);
      setResult(res.data);
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || "Detection failed";
      setError(msg);
    }
    setLoading(false);
  };

  return (
    <div className="card">
      <h2>Plant Disease Detection</h2>

      <label htmlFor="disease-file" className="file-label">
        Choose a leaf image (JPG/PNG)
      </label>
      <input
        id="disease-file"
        type="file"
        accept="image/*"
        onChange={handleFileChange}
      />

      {preview && (
        <div className="preview-container">
          <img
            src={preview}
            alt="Leaf preview"
            className="preview-img"
          />
        </div>
      )}

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Analyzing..." : "Detect Disease"}
      </button>

      {error && <div className="error-msg">⚠️ {error}</div>}

      {result && (
        <div className="result-card success">
          🦠 Disease: <strong>{result.disease}</strong><br />
          📊 Confidence: <strong>{result.confidence}%</strong>
        </div>
      )}
    </div>
  );
}