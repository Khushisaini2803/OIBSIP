import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="WEATHERIQ | Smart Weather",
    page_icon="🌦️",
    layout="wide"
)

# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #101827, #172c46);
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
.metric-card {
    background: rgba(255,255,255,0.08);
    padding: 18px;
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,0.15);
}
</style>
""", unsafe_allow_html=True)

# ---------------- WEATHER CODES ----------------

def weather_condition(code):

    conditions = {
        0: "Clear Sky ☀️",
        1: "Mainly Clear 🌤️",
        2: "Partly Cloudy ⛅",
        3: "Overcast ☁️",
        45: "Foggy 🌫️",
        48: "Depositing Rime Fog 🌫️",
        51: "Light Drizzle 🌦️",
        53: "Moderate Drizzle 🌦️",
        55: "Dense Drizzle 🌧️",
        61: "Slight Rain 🌧️",
        63: "Moderate Rain 🌧️",
        65: "Heavy Rain 🌧️",
        71: "Slight Snow ❄️",
        73: "Moderate Snow ❄️",
        75: "Heavy Snow ❄️",
        80: "Rain Showers 🌧️",
        81: "Moderate Showers 🌧️",
        82: "Heavy Showers ⛈️",
        95: "Thunderstorm ⛈️",
        96: "Thunderstorm with Hail ⛈️",
        99: "Heavy Thunderstorm ⛈️"
    }

    return conditions.get(code, "Unknown Weather")


# ---------------- CITY SEARCH ----------------

@st.cache_data(ttl=600)
def get_city(city):

    url = "https://geocoding-api.open-meteo.com/v1/search"

    response = requests.get(
        url,
        params={
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        },
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    if not data.get("results"):
        return None

    return data["results"][0]


# ---------------- WEATHER DATA ----------------

@st.cache_data(ttl=600)
def get_weather(lat, lon):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": (
            "temperature_2m,relative_humidity_2m,"
            "apparent_temperature,precipitation,"
            "weather_code,wind_speed_10m,uv_index"
        ),
        "hourly": (
            "temperature_2m,precipitation_probability"
        ),
        "daily": (
            "weather_code,temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_probability_max,uv_index_max"
        ),
        "forecast_days": 7,
        "timezone": "auto"
    }

    response = requests.get(
        url, params=params, timeout=20
    )

    response.raise_for_status()

    return response.json()


# ---------------- AIR QUALITY ----------------

@st.cache_data(ttl=600)
def get_air_quality(lat, lon):

    url = "https://air-quality-api.open-meteo.com/v1/air-quality"

    response = requests.get(
        url,
        params={
            "latitude": lat,
            "longitude": lon,
            "current": "us_aqi,pm2_5,pm10"
        },
        timeout=15
    )

    response.raise_for_status()

    return response.json()


# ---------------- SMART SUGGESTIONS ----------------

def smart_suggestions(temp, rain, uv, aqi):

    suggestions = []

    if rain >= 50:
        suggestions.append(
            "🌧️ Rain is likely. Consider carrying an umbrella."
        )

    if temp >= 35:
        suggestions.append(
            "☀️ High temperature. Stay hydrated and avoid prolonged heat."
        )

    elif temp <= 10:
        suggestions.append(
            "🧥 Cold conditions. Wear suitable warm clothing."
        )

    if uv >= 6:
        suggestions.append(
            "🕶️ UV level is high. Sun protection is recommended."
        )

    if aqi is not None and aqi > 100:
        suggestions.append(
            "🌫️ Air quality may be unhealthy for sensitive groups."
        )

    if not suggestions:
        suggestions.append(
            "✅ No major weather alert based on the available data."
        )

    return suggestions


# ---------------- MAIN APP ----------------

def main():

    st.title("🌦️ WEATHERIQ")
    st.subheader("Smart Weather Intelligence Dashboard")

    st.caption(
        "Live Weather | Forecast | Air Quality | Weather Analytics"
    )

    st.divider()

    city = st.text_input(
        "🔍 Search Your City",
        placeholder="Enter city name (e.g. Delhi, Mumbai, London)"
    )

    search = st.button(
        "Get Weather",
        type="primary",
        use_container_width=True
    )

    if search:

        if not city.strip():
            st.warning("Please enter a city name.")
            return

        try:

            with st.spinner("Finding city..."):

                location = get_city(city.strip())

            if location is None:
                st.error("City not found. Please try another name.")
                return

            lat = location["latitude"]
            lon = location["longitude"]

            with st.spinner("Fetching live weather data..."):

                weather = get_weather(lat, lon)

            air = None

            try:
                air = get_air_quality(lat, lon)
            except requests.RequestException:
                st.info("Air quality data is temporarily unavailable.")

            current = weather["current"]
            hourly = weather["hourly"]
            daily = weather["daily"]

            st.session_state["weather"] = weather
            st.session_state["location"] = location
            st.session_state["air"] = air

        except requests.RequestException as error:

            st.error(f"Network error: {error}")
            return

        except (KeyError, ValueError, TypeError) as error:

            st.error(f"Unable to process weather data: {error}")
            return

    # ---------------- DISPLAY DATA ----------------

    if "weather" not in st.session_state:
        st.info("Enter a city name and click Get Weather.")
        return

    weather = st.session_state["weather"]
    location = st.session_state["location"]
    air = st.session_state["air"]

    current = weather["current"]
    hourly = weather["hourly"]
    daily = weather["daily"]

    place = location["name"]
    country = location.get("country", "")

    st.divider()

    st.markdown(f"## 📍 {place}, {country}")

    st.caption(
        f"Local Weather Time: {current['time']}"
    )

    condition = weather_condition(
        current["weather_code"]
    )

    st.markdown(f"### {condition}")

    # ---------------- CURRENT WEATHER ----------------

    st.markdown("## 🌡️ Current Weather")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Temperature",
        f"{current['temperature_2m']} °C"
    )

    col2.metric(
        "Feels Like",
        f"{current['apparent_temperature']} °C"
    )

    col3.metric(
        "Humidity",
        f"{current['relative_humidity_2m']} %"
    )

    col4.metric(
        "Wind Speed",
        f"{current['wind_speed_10m']} km/h"
    )

    col5, col6, col7 = st.columns(3)

    col5.metric(
        "UV Index",
        current["uv_index"]
    )

    col6.metric(
        "Precipitation",
        f"{current['precipitation']} mm"
    )

    if air and air.get("current"):

        air_data = air["current"]

        col7.metric(
            "US AQI",
            air_data.get("us_aqi", "N/A")
        )

    else:

        col7.metric("US AQI", "Unavailable")

    # ---------------- AIR QUALITY ----------------

    st.divider()

    st.markdown("## 🌍 Air Quality Information")

    if air and air.get("current"):

        air_data = air["current"]

        a, b, c = st.columns(3)

        a.metric(
            "US AQI",
            air_data.get("us_aqi", "N/A")
        )

        b.metric(
            "PM2.5",
            f"{air_data.get('pm2_5', 'N/A')} µg/m³"
        )

        c.metric(
            "PM10",
            f"{air_data.get('pm10', 'N/A')} µg/m³"
        )

        st.caption(
            "AQI is based on the US AQI scale."
        )

    else:

        st.info("Air quality information is unavailable.")

    # ---------------- HOURLY FORECAST ----------------

    st.divider()

    st.markdown("## ⏰ Next 24 Hours")

    hourly_df = pd.DataFrame({
        "Time": pd.to_datetime(hourly["time"][:24]),
        "Temperature": hourly["temperature_2m"][:24],
        "Rain Probability": hourly[
            "precipitation_probability"
        ][:24]
    })

    fig = px.line(
        hourly_df,
        x="Time",
        y="Temperature",
        title="Hourly Temperature Forecast",
        markers=True,
        template="plotly_dark"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---------------- SEVEN DAY FORECAST ----------------

    st.divider()

    st.markdown("## 📅 7-Day Weather Forecast")

    forecast_df = pd.DataFrame({
        "Date": daily["time"],
        "Condition": [
            weather_condition(code)
            for code in daily["weather_code"]
        ],
        "Max Temperature": daily["temperature_2m_max"],
        "Min Temperature": daily["temperature_2m_min"],
        "Rain Probability": daily[
            "precipitation_probability_max"
        ],
        "UV Index": daily["uv_index_max"]
    })

    st.dataframe(
        forecast_df,
        use_container_width=True,
        hide_index=True
    )

    # ---------------- SMART SUGGESTIONS ----------------

    st.divider()

    st.markdown("## 💡 Smart Weather Insights")

    rain_probability = daily[
        "precipitation_probability_max"
    ][0]

    aqi = None

    if air and air.get("current"):
        aqi = air["current"].get("us_aqi")

    suggestions = smart_suggestions(
        current["temperature_2m"],
        rain_probability,
        current["uv_index"],
        aqi
    )

    for suggestion in suggestions:
        st.info(suggestion)

    # ---------------- FOOTER ----------------

    st.divider()

    st.caption(
        "WEATHERIQ | Built with Python, Streamlit, "
        "Open-Meteo API, Pandas and Plotly"
    )

    st.caption(
        "Weather forecasts are estimates and may change."
    )


if __name__ == "__main__":
    main()