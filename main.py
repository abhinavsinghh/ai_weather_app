from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv()


def get_weather(city:str):
    '''get weather for a given city'''
    return 'sunny'

def get_location():
    '''Get user's current location. Use this when the user not specified any location'''
    return 'Delhi, India'

llm = ChatGoogleGenerativeAI(
    model = 'gemini-2.5-flash',
    temperature = 0.4,
)

system_prompt = '''
You are a helpful weather assistant.

YOUR WORKFLOW:
1. If the user asks about weather without giving you the current location, you must:
- Use the get location tool to get the loation of the user

If the user specifies the location in the prompt:
- Use that location directly in get_weather tool
'''




agent = create_agent(
    model = llm,
    tools = [get_weather, get_location]
)

user_query = input("Enter you Query: ")

response1 = agent.invoke(
    {"messages": [{'role': 'user',
                   'content': user_query}]})
print(response1['messages'][-1].content)