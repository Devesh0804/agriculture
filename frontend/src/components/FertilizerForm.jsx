// src/components/FertilizerForm.jsx
import { useState } from "react";
import { predictFertilizer } from "../api";

export default function FertilizerForm() {
  const [form, setForm] = useState({
    N: "", P: "", K: "", ph: "", temperature: "", humidity: "", rainfall: "", crop: "",
  });
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async () => {
    setError("");
    setResult(null);

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
        crop: form.crop.trim(),
      };

      const res = await predictFertilizer(payload);
      setResult({
        fertilizer: res.data.fertilizer_type,
        quantity: res.data.quantity,
      });
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || "Prediction failed";
      setError(msg);
    }
    setLoading(false);
  };

  const numericFields = [
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
      <h2>Fertilizer Recommendation</h2>

      <div className="form-grid">
        {numericFields.map((f) => (
          <div key={f.name} className="field">
            <label htmlFor={`fert-${f.name}`}>{f.label}</label>
            <input
              id={`fert-${f.name}`}
              name={f.name}
              type="number"
              step="any"
              placeholder={f.label}
              value={form[f.name]}
              onChange={handleChange}
            />
          </div>
        ))}
        <div className="field">
          <label htmlFor="fert-crop">Crop Name</label>
          <input
            id="fert-crop"
            name="crop"
            type="text"
            placeholder="e.g. rice, wheat, maize"
            value={form.crop}
            onChange={handleChange}
          />
        </div>
      </div>

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Predicting..." : "Predict Fertilizer"}
      </button>

      {error && <div className="error-msg">⚠️ {error}</div>}

      {result && (
        <div className="result-card success">
          🧪 Fertilizer: <strong>{result.fertilizer}</strong><br />
          📦 Quantity: <strong>{result.quantity.toFixed(2)} kg/hectare</strong>
        </div>
      )}
    </div>
  );
}