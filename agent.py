import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key="AIzaSyC6Ro1Go0wa_QrnVN3PDt5Je2ff3c9tfjk")

model = genai.GenerativeModel("gemini-3.5-flash")

def ask_agent(question, weather_data):

    prompt = f"""
    You are a Weather AI Assistant.

    Weather Data:
    {weather_data}

    User Question:
    {question}

    Give weather advice naturally.
    """

    response = model.generate_content(prompt)

    return response.text