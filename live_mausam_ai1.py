import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from pymongo import MongoClient

# Load data from MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["live_weather_db"]
collection = db["live_weather_data"]
data = pd.DataFrame(list(collection.find()))

# Ensure necessary columns
required_columns = ["city", "temperature_C", "humidity", "weather"]
if not all(col in data.columns for col in required_columns):
    raise ValueError("Missing required columns in the dataset")

# Encode the target variable (weather condition)
label_encoder = LabelEncoder()
data['weather_encoded'] = label_encoder.fit_transform(data['weather'])

# Prepare features and labels
X = data[['temperature_C', 'humidity']]
y = data['weather_encoded']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Accuracy
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"\nModel Accuracy: {accuracy * 100:.2f}%\n")

# Full prediction on entire data
data['predicted_weather'] = label_encoder.inverse_transform(model.predict(X))

# Print clear prediction results per city
print("City-wise Weather Predictions:\n")
print(data[['city', 'temperature_C', 'humidity', 'weather', 'predicted_weather']].to_string(index=False))

# Scatter plot with city labels
plt.figure(figsize=(14, 8))
sns.scatterplot(data=data, x='temperature_C', y='humidity', hue='predicted_weather', palette='Set2', s=120, edgecolor='black')

# Add city name labels
for i in range(data.shape[0]):
    plt.text(
        x=data['temperature_C'].iloc[i] + 0.1,
        y=data['humidity'].iloc[i] + 0.1,
        s=data['city'].iloc[i],
        fontsize=9,
        color='black',
        weight='bold'
    )

plt.title("Predicted Weather per City Based on Temperature and Humidity")
plt.xlabel("Temperature (°C)")
plt.ylabel("Humidity (%)")
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(title="Predicted Weather", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
