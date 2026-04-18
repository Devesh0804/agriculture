import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("data/processed_fertilizer.csv")

X = df[['N', 'P', 'K', 'pH', 'temperature', 'humidity', 'rainfall', 'crop']]
y = df['fertilizer']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


model = RandomForestClassifier(
    n_estimators=100,
    class_weight='balanced',
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy)
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Create quantity (simple engineered feature)
df['quantity'] = (
    (150 - df['N']) * 0.3 +
    (80 - df['P']) * 0.3 +
    (80 - df['K']) * 0.4
)

# Ensure no negative values
df['quantity'] = df['quantity'].apply(lambda x: max(x, 0))

joblib.dump(model, 'models/fertilitly_type_model.pkl')