import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# MongoDB Connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["live_weather_db"]
collection = db["live_weather_data"]

# Fetch Data from MongoDB
data = list(collection.find({}, {"_id": 0}))
df = pd.DataFrame(data)

# Ensure 'date' exists
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date')
else:
    print("❌ Warning: 'date' column is missing!")
    df['date'] = pd.NaT

# Plot Temperature Trends for Multiple Cities
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x='date', y='temperature_C', hue='city', marker="o")
plt.xlabel("Date & Time")
plt.ylabel("Temperature (°C)")
plt.title("Live Weather Temperature Trends (Multiple Cities)")
plt.xticks(rotation=45)
plt.legend(title="City")
plt.grid()
plt.show()
