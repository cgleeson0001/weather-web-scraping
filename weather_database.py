import sqlite3
import pandas as pd

# Load CSV files into Pandas DataFrames
raw_df = pd.read_csv("weather_raw.csv")
clean_df = pd.read_csv("weather_cleaned.csv")

print("Raw weather data:")
print(raw_df.head())

print("\nCleaned weather data:")
print(clean_df.head())

try:
    conn = sqlite3.connect("weather.db")

    # Save each CSV to a separate SQLite table
    raw_df.to_sql(
        "weather_raw",
        conn,
        if_exists="replace",
        index=False
    )

    clean_df.to_sql(
        "weather_cleaned",
        conn,
        if_exists="replace",
        index=False
    )

    conn.commit()
    print("\nWeather data saved to SQLite successfully.")

except sqlite3.Error as e:
    print("Database error:", e)

finally:
    if "conn" in locals():
        conn.close()
        