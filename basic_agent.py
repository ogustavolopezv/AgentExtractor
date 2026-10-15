import requests

from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.tools import tool


@tool('get_weather', description='Return weather information for a given city', return_direct=False)
def get_weather(city: str):
    response = requests.get(f'https://wttr.in/{city}?format=j1')
    return response.json()

model = ChatOllama(model="llama3.1:8b")
model = model.bind_tools([get_weather])

agent = create_agent(
    model = model,
    tools = [get_weather],
    system_prompt = 'You are a  helpful weather assistant, who always cracks jokes and is humorous while remaining helpful.' 
)

response = agent.invoke({
    'messages': [
        {'role': 'user', 'content': 'What is the weather like in León, Guanajuato?'}
    ]
})

print(response['messages'][-1].content)