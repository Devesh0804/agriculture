import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# Load processed data
df = pd.read_csv("data/processed_fertilizer.csv")

# Features and target
X = df[['N', 'P', 'K', 'pH', 'temperature', 'humidity', 'rainfall', 'crop']]
y = df['quantity']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluation
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("MAE:", mae)
print("R2 Score:", r2)

# Save model
joblib.dump(model, "models/fertilizer_quantity_model.pkl")

print("\nQuantity model saved ✅")