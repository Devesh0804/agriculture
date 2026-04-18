// src/components/FertilizerForm.jsx
import { useState } from "react";
import { predictFertilizer } from "../api";

export default function FertilizerForm() {
  const [form, setForm] = useState({
    N: "", P: "", K: "", ph: "", temperature: "", humidity: "", rainfall: "", crop: ""
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const payload = {
        ...form,
        N: Number(form.N),
        P: Number(form.P),
        K: Number(form.K),
        ph: Number(form.ph),
        temperature: Number(form.temperature),
        humidity: Number(form.humidity),
        rainfall: Number(form.rainfall),
      };

      const res = await predictFertilizer(payload);

      // ✅ FIXED KEY (your backend uses fertilizer_type)
      setResult({
        fertilizer: res.data.fertilizer_type,
        quantity: res.data.quantity,
      });

    } catch (err) {
      console.error(err);
      setResult(null);
    }
    setLoading(false);
  };

  return (
    <div className="card">
      <h2>Fertilizer Recommendation</h2>

      {["N","P","K","ph","temperature","humidity","rainfall","crop"].map((f) => (
        <input
          key={f}
          name={f}
          placeholder={f}
          value={form[f]}
          onChange={handleChange}
        />
      ))}

      <button onClick={handleSubmit}>
        {loading ? "Loading..." : "Predict"}
      </button>

      {result && (
        <div className="card">
          🌿 Fertilizer: {result.fertilizer} <br />
          Quantity: {result.quantity.toFixed(2)}
        </div>
      )}
    </div>
  );
}