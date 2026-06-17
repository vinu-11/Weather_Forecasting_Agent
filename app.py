import streamlit as st
import pandas as pd
import plotly.express as px
import speech_recognition as sr

from weather_tools import *
from agent import ask_agent

st.set_page_config(page_title="Weather AI Agent")

st.title("🌦️ Agentic Weather AI")

city = st.text_input("Enter City")

voice = st.button("🎤 Voice Input")

question = ""

if voice:

    r = sr.Recognizer()

    with sr.Microphone() as source:

        st.write("Listening...")

        audio = r.listen(source)

        try:
            question = r.recognize_google(audio)
            st.success(question)

        except:
            st.error("Could not understand.")

question = st.text_input(
    "Ask weather question",
    value=question
)

if city:

    try:
        current = get_current_weather(city)

        st.subheader("Current Weather")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Temperature",
            f"{current['temperature']} °C"
        )

        col2.metric(
            "Humidity",
            f"{current['humidity']} %"
        )

        col3.metric(
            "Wind",
            f"{current['wind_speed']} m/s"
        )

        st.write("Condition:", current["condition"])

        forecast = get_forecast(city)

        df = pd.DataFrame(forecast)

        st.subheader("7-Day Forecast")

        st.dataframe(df.head(56))

        st.subheader("Temperature Trend")

        fig = px.line(
            df,
            x="datetime",
            y="temp"
        )

        st.plotly_chart(fig)

        st.subheader("Rain Prediction")

        rain_fig = px.bar(
            df,
            x="datetime",
            y="rain"
        )

        st.plotly_chart(rain_fig)

        max_rain = df["rain"].max()

        if max_rain > 60:
            st.warning("High probability of rain.")

        lat, lon = get_coordinates(city)

        aqi = get_air_quality(lat, lon)

        st.subheader("Air Quality")

        st.metric(
            "AQI",
            aqi["main"]["aqi"]
        )

        if aqi["main"]["aqi"] >= 4:
            st.error("Poor air quality alert.")

        st.subheader("Weather Alerts")

        if current["wind_speed"] > 10:
            st.warning("Strong wind alert")

        if current["temperature"] > 38:
            st.error("Heat wave alert")

        if question:

            weather_context = {
                "current": current,
                "forecast": forecast[:10],
                "aqi": aqi
            }

            answer = ask_agent(
                question,
                weather_context
            )

            st.subheader("AI Response")

            st.write(answer)

    except Exception:
        st.error(
            f"❌ City '{city}' not found. Please enter a valid city name."
        )