# weather-web-scraping

This project uses Selenium to scrape current weather data from the Timeanddate.com "Weather Around the World" page.

## Data Collected

The scraper collects data for approximately 140 cities:

- City
- Day
- Local time
- Temperature in Fahrenheit

The scraped data is loaded into a Pandas DataFrame and saved to CSV.

## Data Cleaning

Pandas is used to:
- Remove duplicate records
- Remove missing values
- Store temperature as numeric data
- Display the data before and after cleaning

## Files

- `weather_scraper.py` - Web scraping and data cleaning code
- `weather_raw.csv` - Raw weather data
- `weather_cleaned.csv` - Cleaned weather data
- `requirements.txt` - Project dependencies

## Setup

Install the required packages:

```bash
pip install -r requirements.txt