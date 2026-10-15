from dataclasses import dataclass

import requests

from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import InMemorySaver

@dataclass
class Context:
    user_id: str

# @dataclass
# class ResponseFormat:
#     summary: str
#     temperature_celsius: float

@tool('get_weather', description='Return weather information for a given city', return_direct=False)
def get_weather(city: str):
    response = requests.get(f'https://wttr.in/{city}?format=j1')
    return response.json()

@tool('locate_user', description="Look up a user's city based on the context")
def locate_user(runtime= ToolRuntime[Context]):
    match runtime.context.user_id:
        case 'A1':
            return 'London' 
        case 'B2':
            return 'León, Guanajuato'
        case _:
            return 'Unknown'

model = ChatOllama(model="llama3.1:8b", temperature=0)
model = model.bind_tools([get_weather, locate_user])

checkpointer = InMemorySaver()

agent = create_agent(
    model = model,
    tools = [get_weather, locate_user], 
    system_prompt = 'You are a helpful weather assistant, who always cracks jokes and is humorous while remaining helpful.',
    context_schema = Context,
    checkpointer = checkpointer
    #response_format = ResponseFormat,
)

config = {'configurable': {'thread_id': 1}}

response = agent.invoke({
    'messages': [
        {'role': 'user', 'content': "Where am I?"}
    ]},
    config = config,
    context = Context(user_id='B2')
)


#print(response)
#print(response['structured_response'])
print('---------------------------------')
print(response['messages'][-1].content)