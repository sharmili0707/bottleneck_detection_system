import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
data = pd.read_csv("dataset/supply_chain_data.csv")


data['Delay'] = (data['Days for shipping (real)'] > data['Days for shipment (scheduled)']).astype(int)

# Select features
features = [
    'Days for shipping (real)',
    'Days for shipment (scheduled)',
    'Order Item Quantity',
    'Sales'
]

X = data[features]
y = data['Delay']

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
with open("models/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved!")