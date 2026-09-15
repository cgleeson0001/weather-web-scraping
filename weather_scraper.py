# Web Scraping Capstone - Weather Around the World

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

url = "https://www.timeanddate.com/weather/"

# Start Chrome
service = Service(ChromeDriverManager().install())

options = webdriver.ChromeOptions()
options.page_load_strategy = "eager"

driver = webdriver.Chrome(
    service=service,
    options=options
)

print("Opening website...")
driver.get(url)
print("Website loaded.")

# Find the weather table
table = driver.find_element(
    By.CSS_SELECTOR,
    "table.zebra.fw.tb-theme"
)

# Get all table text at once
table_text = table.text

# Close Selenium immediately
driver.quit()

print("\nSCRAPED DATA:")
print(table_text[:1000])

# Save the raw scraped data
with open("weather_raw.txt", "w", encoding="utf-8") as file:
    file.write(table_text)

print("\nRaw weather data saved.")

import re

# Match city, day, time, and temperature
pattern = r"(.+?)\s+\*?\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+(\d{1,2}:\d{2}\s*[ap]m)\s+(-?\d+)\s*°F"

matches = re.findall(pattern, table_text)

weather_data = []

for city, day, local_time, temperature in matches:
    weather_data.append({
        "City": city.strip(),
        "Day": day,
        "Local Time": local_time,
        "Temperature_F": int(temperature)
    })

# Create DataFrame
df = pd.DataFrame(weather_data)

print("\nBEFORE CLEANING:")
print(df.head())
print("Rows:", len(df))

# Save raw data
df.to_csv("weather_raw.csv", index=False)

# Basic cleaning
clean_df = df.drop_duplicates()
clean_df = clean_df.dropna()

print("\nAFTER CLEANING:")
print(clean_df.head())
print("Rows:", len(clean_df))

clean_df.to_csv("weather_cleaned.csv", index=False)

print("\nCSV files created successfully.")