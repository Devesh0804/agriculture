// src/components/CropForm.jsx
import { useState } from "react";
import { predictCrop } from "../api";

export default function CropForm() {
  const [form, setForm] = useState({
    N: "", P: "", K: "", ph: "", temperature: "", humidity: "", rainfall: ""
  });
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async () => {
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

      console.log("Sending:", payload);

      const res = await predictCrop(payload);

      console.log("Response:", res.data);

      // FIX: handle different backend response formats
      setResult(
        res.data.prediction ||
        res.data.crop ||
        res.data.result ||
        JSON.stringify(res.data)
      );

    } catch (err) {
      console.error(err);
      setResult("Error fetching prediction");
    }
    setLoading(false);
  };

  return (
    <div className="card">
      <h2>Crop Recommendation</h2>

      {["N","P","K","ph","temperature","humidity","rainfall"].map((f) => (
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
          🌱 {result}
        </div>
      )}
    </div>
  );
}