import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st


# Page setup
st.set_page_config(
    page_title="Global Weather Dashboard",
    page_icon="🌤️",
    layout="wide"
)

st.title("🌤️ Global Weather Dashboard")

st.write(
    "Explore temperature data collected from the Timeanddate.com "
    "Weather Around the World page."
)


# Load cleaned weather data from SQLite
@st.cache_data
def load_data():
    conn = sqlite3.connect("weather.db")
    df = pd.read_sql_query(
        "SELECT * FROM weather_cleaned",
        conn
    )
    conn.close()
    return df


df = load_data()


# Sidebar filters
st.sidebar.header("Filter Weather Data")

cities = sorted(df["City"].unique())

selected_cities = st.sidebar.multiselect(
    "Select cities",
    cities,
    default=cities
)

min_temp = int(df["Temperature_F"].min())
max_temp = int(df["Temperature_F"].max())

temperature_range = st.sidebar.slider(
    "Temperature range (°F)",
    min_value=min_temp,
    max_value=max_temp,
    value=(min_temp, max_temp)
)


# Apply filters
filtered_df = df[
    (df["City"].isin(selected_cities))
    & (df["Temperature_F"] >= temperature_range[0])
    & (df["Temperature_F"] <= temperature_range[1])
]


# Summary metrics
st.subheader("Weather Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Cities Displayed", len(filtered_df))

with col2:
    if not filtered_df.empty:
        st.metric(
            "Average Temperature",
            f"{filtered_df['Temperature_F'].mean():.1f} °F"
        )
    else:
        st.metric("Average Temperature", "N/A")

with col3:
    if not filtered_df.empty:
        st.metric(
            "Highest Temperature",
            f"{filtered_df['Temperature_F'].max()} °F"
        )
    else:
        st.metric("Highest Temperature", "N/A")


if filtered_df.empty:
    st.warning("No weather records match the selected filters.")

else:

    # Visualization 1
    st.subheader("Temperature by City")

    city_chart = px.bar(
        filtered_df.sort_values("Temperature_F"),
        x="City",
        y="Temperature_F",
        title="Temperature by City",
        labels={"Temperature_F": "Temperature (°F)"}
    )

    st.plotly_chart(city_chart, use_container_width=True)


    # Visualization 2
    st.subheader("Temperature Distribution")

    histogram = px.histogram(
        filtered_df,
        x="Temperature_F",
        nbins=20,
        title="Distribution of Temperatures",
        labels={"Temperature_F": "Temperature (°F)"}
    )

    st.plotly_chart(histogram, use_container_width=True)


    # Visualization 3
    st.subheader("Cities by Temperature")

    scatter = px.scatter(
        filtered_df,
        x="City",
        y="Temperature_F",
        hover_data=["Day", "Local Time"],
        title="City Temperature Comparison",
        labels={"Temperature_F": "Temperature (°F)"}
    )

    st.plotly_chart(scatter, use_container_width=True)


# Data table
with st.expander("View Weather Data"):
    st.dataframe(filtered_df, use_container_width=True)