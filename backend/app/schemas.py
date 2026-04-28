from pydantic import BaseModel, Field


class CropRequest(BaseModel):
    N: float = Field(ge=0, description="Nitrogen content")
    P: float = Field(ge=0, description="Phosphorus content")
    K: float = Field(ge=0, description="Potassium content")
    temperature: float = Field(description="Temperature in Celsius")
    humidity: float = Field(ge=0, le=100, description="Humidity percentage")
    rainfall: float = Field(ge=0, description="Rainfall in mm")
    ph: float = Field(ge=0, le=14, description="Soil pH level")


class CropResponse(BaseModel):
    crop: str


class FertilizerRequest(CropRequest):
    crop: str = Field(min_length=1, description="Crop name")


class FertilizerResponse(BaseModel):
    fertilizer_type: str
    quantity: float


class DiseaseResponse(BaseModel):
    disease: str
    confidence: float