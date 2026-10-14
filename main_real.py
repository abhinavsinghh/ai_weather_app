from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.agents import create_agent
import os
import requests
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.sqlite import SqliteSaver

load_dotenv()

DB_URI = os.getenv("SUPERBASE_DB_URI")

def get_weather(city:str):
    '''get weather for a given city'''
    api_key = os.getenv('OPENWEATHER_API_KEY')
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data

# def get_location():
#     '''Get user's current location. Use this when the user not specified any location'''
#     response = requests.get('https://ipapi.co/json/', headers={'User-agent': 'your bot 0.1'})
#     data = response.json()
#     city = data['city']
#     country = data['country_name']
#     return f"{city}, {country}"
 
def get_location():
    from flask import session
    '''use this when user asks about weather without specifing a location'''
    lat = session['user_location']['lat']
    lon = session['user_location']['lon']

    response = request.get(f'https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json',
                           headers = {'User-Agent': 'WeatherAssistant/1.0'}, timeout=3)
    data = response.json()
    print(data)
    city = data['address'].get('city', data['address'].get('town', 'Unknown'))
    country = data['address'].get('country', ' ')
    return f'{city}, {country}'
    
llm = ChatGoogleGenerativeAI(
    model = 'gemini-2.5-flash',
    temperature = 0.4,
)

system_prompt = '''
You are a helpful weather assistant.

YOUR WORKFLOW:
1. If the user asks about weather without giving you the current location, you must:
- Use the get location tool to get the loation of the user

2. If the user specifies the location in the prompt:
- Use that location directly in get_weather tool

3. Use your knowledge to determine which temprature unit is standard for the given location

4. Present the weather information including temperature, condition, wind speed and any other relevant information
'''

connection = SqliteSaver.from_conn_string('checkpoints.db')
checkpointer = connection.__enter__()
agent = create_agent(
        model = llm,
        tools = [get_weather, get_location],
        system_prompt=system_prompt,
        checkpointer=checkpointer
    )



    