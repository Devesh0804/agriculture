// src/components/CropForm.jsx
import { useState } from "react";
import { predictCrop } from "../api";

export default function CropForm() {
  const [form, setForm] = useState({
    N: "", P: "", K: "", ph: "", temperature: "", humidity: "", rainfall: "",
  });
  const [result, setResult] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async () => {
    setError("");
    setResult("");

    // Basic validation
    const empty = Object.entries(form).filter(([, v]) => v === "");
    if (empty.length > 0) {
      setError(`Please fill in: ${empty.map(([k]) => k).join(", ")}`);
      return;
    }

    setLoading(true);
    try {
      const payload = {
        N: Number(form.N),
        P: Number(form.P),
        K: Number(form.K),
        ph: Number(form.ph),
        temperature: Number(form.temperature),
        humidity: Number(form.humidity),
        rainfall: Number(form.rainfall),
      };

      const res = await predictCrop(payload);
      setResult(res.data.crop || JSON.stringify(res.data));
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || "Prediction failed";
      setError(msg);
    }
    setLoading(false);
  };

  const fields = [
    { name: "N", label: "Nitrogen (N)" },
    { name: "P", label: "Phosphorus (P)" },
    { name: "K", label: "Potassium (K)" },
    { name: "ph", label: "Soil pH" },
    { name: "temperature", label: "Temperature (°C)" },
    { name: "humidity", label: "Humidity (%)" },
    { name: "rainfall", label: "Rainfall (mm)" },
  ];

  return (
    <div className="card">
      <h2>Crop Recommendation</h2>

      <div className="form-grid">
        {fields.map((f) => (
          <div key={f.name} className="field">
            <label htmlFor={`crop-${f.name}`}>{f.label}</label>
            <input
              id={`crop-${f.name}`}
              name={f.name}
              type="number"
              step="any"
              placeholder={f.label}
              value={form[f.name]}
              onChange={handleChange}
            />
          </div>
        ))}
      </div>

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Predicting..." : "Predict Crop"}
      </button>

      {error && <div className="error-msg">⚠️ {error}</div>}

      {result && (
        <div className="result-card success">
          🌱 Recommended Crop: <strong>{result}</strong>
        </div>
      )}
    </div>
  );
}