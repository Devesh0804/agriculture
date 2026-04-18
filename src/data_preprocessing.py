import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

# crop recommendation data

df = pd.read_csv("data/crop_data.csv")

print("Missing values:\n", df.isnull().sum())

df = df.dropna()

X = df.drop("label", axis=1)
y = df["label"]

print("\nFeatures shape:", X.shape)
print("Target shape:", y.shape)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("\nTrain shape", X_train.shape)
print("Test shape", X_test.shape)

# fertilizer recommendation data

df = pd.read_csv("data/fertilizer_data.csv")

df = df[[
    'Nitrogen_Level',
    'Phosphorus_Level',
    'Potassium_Level',
    'Soil_pH',
    'Temperature',
    'Humidity',
    'Rainfall',
    'Crop_Type',
    'Recommended_Fertilizer'
]]

df.columns = [
    'N', 'P', 'K', 'pH',
    'temperature', 'humidity', 'rainfall',
    'crop', 'fertilizer'
]

print("Columns after renaming:")
print(df.columns)

df = df.dropna()

# Normalize crop names
df['crop'] = df['crop'].str.lower().str.strip()

crop_encoder = LabelEncoder()
fert_encoder = LabelEncoder()

df['crop'] = crop_encoder.fit_transform(df['crop'])
df['fertilizer'] = fert_encoder.fit_transform(df['fertilizer'])



# Save encoders
joblib.dump(crop_encoder, "models/crop_encoder.pkl")
joblib.dump(fert_encoder, "models/fertilizer_encoder.pkl")

# Create quantity (engineered feature)
df['quantity'] = (
    (150 - df['N']) * 0.3 +
    (80 - df['P']) * 0.3 +
    (80 - df['K']) * 0.4
)

# Avoid negative values
df['quantity'] = df['quantity'].apply(lambda x: max(x, 0))


df.to_csv("data/processed_fertilizer.csv", index=False)
print("Preprocessing done ✅")