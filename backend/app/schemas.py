from pydantic import BaseModel


class CropRequest(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    rainfall: float
    ph: float


class CropResponse(BaseModel):
    crop: str


class FertilizerRequest(CropRequest):
    crop: str


class FertilizerResponse(BaseModel):
    fertilizer_type: str
    quantity: float


class DiseaseResponse(BaseModel):
    disease: str
    confidence: float