import pymongo
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# 🔹 Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["weather_db"]
collection = db["weather_data"]

# 🔹 Fetch Data from MongoDB
data = list(collection.find({}, {"_id": 0}))  # Exclude _id
df = pd.DataFrame(data)

# 🔹 Check if data exists
if df.empty:
    print("❌ No data found in MongoDB. Please run the weather app first!")
    exit()

# 🔹 Selecting Features and Target
X = df[['temperature_C']]  # Feature
y = df['temperature_C'].shift(-1).fillna(df['temperature_C'].mean())  # Target (Next day's temp)

# 🔹 Splitting Data into Training & Testing Sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🔹 Train Model
model = LinearRegression()
model.fit(X_train, y_train)

# 🔹 Predict
y_pred = model.predict(X_test)

# 🔹 Evaluate Model
error = mean_absolute_error(y_test, y_pred)
print(f"✅ Model Trained! Mean Absolute Error: {error:.2f}°C")

# 🔹 Save the Model (Optional)
import joblib
joblib.dump(model, "weather_model.pkl")
print("✅ Model Saved as 'weather_model.pkl'")
