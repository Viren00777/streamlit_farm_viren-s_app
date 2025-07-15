import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
import requests
st.set_page_config(page_title="Smart Farming Advisor", layout="wide")

st.title("🌾 Smart Farming Insights Tool By Viren")
st.markdown("Upload your farm data Excel file to get insights on crop yield, fertilizer usage, and more.")

uploaded_file = st.file_uploader("📤 Upload Excel file (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("✅ File Uploaded Successfully!")

    st.subheader("📋 Data Preview")
    st.dataframe(df)

    # Add calculated column
    df["Yield per Acre"] = df["Yield (kg)"] / df["Area (Acres)"]

    # Average Yield per Crop
    st.subheader("🌱 Average Yield per Crop")
    avg_yield = df.groupby("Crop Type")["Yield (kg)"].mean().sort_values(ascending=False)
    st.bar_chart(avg_yield)

    # Fertilizer Effectiveness
    st.subheader("💊 Fertilizer Effectiveness")
    fert_yield = df.groupby("Fertilizer Used")["Yield (kg)"].mean().sort_values(ascending=False)
    st.bar_chart(fert_yield)

    # Yield per Acre Table
    st.subheader("📊 Yield Efficiency per Acre")
    st.dataframe(df[["Farmer Name", "Crop Type", "Yield per Acre"]])

    # Rainfall vs Yield
    st.subheader("🌧️ Rainfall vs Yield Chart")
    fig1, ax1 = plt.subplots()
    sns.scatterplot(data=df, x="Rainfall (mm)", y="Yield (kg)", hue="Crop Type", ax=ax1)
    st.pyplot(fig1)

    # Crop Recommendation based on Soil Type
    st.subheader("🧠 Crop Recommendation Based on Soil")

    def recommend_crop(soil):
        match soil:
            case "Loamy": return "Wheat, Brinjal, Tomato"
            case "Black Soil": return "Cotton, Pomegranate, Banana"
            case "Sandy": return "Ladyfinger, Groundnut"
            case "Clay": return "Rice, Tomato"
            case _: return "Crop not found"

    df["Recommended Crop"] = df["Soil Type"].apply(recommend_crop)
    st.dataframe(df[["Farmer Name", "Soil Type", "Recommended Crop"]])
    st.subheader("🌦 Real-Time Weather in Pune")

def get_weather_data(city_name, api_key):
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city_name}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            "location": data["location"]["name"],
            "temp_c": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
            "humidity": data["current"]["humidity"],
            "wind_kph": data["current"]["wind_kph"]
        }
    else:
        return None

# Use your actual API key and default to Pune
api_key = "66ca05ace8d04beeaf2153306251507"
city = "Pune"

weather = get_weather_data(city, api_key)

if weather:
    st.success(f"📍 Weather in {weather['location']}")
    st.write(f"🌡 Temperature: {weather['temp_c']} °C")
    st.write(f"☁ Condition: {weather['condition']}")
    st.write(f"💧 Humidity: {weather['humidity']}%")
    st.write(f"🌬 Wind Speed: {weather['wind_kph']} km/h")
else:
    st.error("⚠ Could not fetch weather data. Please check your API key or internet.")

    # Download updated data
    st.download_button(
        label="📥 Download Updated Excel with Insights",
        data=df.to_excel(index=False, engine='openpyxl'),
        file_name='updated_farming_data.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )