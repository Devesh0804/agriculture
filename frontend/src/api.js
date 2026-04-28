// src/api.js
import axios from "axios";

const API = axios.create({
  baseURL: "/api",
});

export const predictCrop = (data) => API.post("/predict-crop", data);
export const predictFertilizer = (data) => API.post("/predict-fertilizer", data);
export const predictDisease = (formData) =>
  API.post("/predict-disease", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
