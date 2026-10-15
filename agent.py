from dataclasses import dataclass
from pathlib import Path

from stt import get_this_stt

from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import InMemorySaver

@dataclass
class Context:
    user_id: str
    speech: str

@dataclass
class ResponseFormat:
    summary: str
    speech: str
    audio_path: str
    transcription: str

@tool('get_stt', description="Return the stt for a speech given its audio path.", return_direct=False)
def get_stt(audio_path: str):
    return get_this_stt(audio_path)

model = ChatOllama(model="llama3.1:8b", temperature=0)
model = model.bind_tools([get_stt])

checkpointer = InMemorySaver()

agent = create_agent(
    model = model,
    tools = [get_stt], 
    system_prompt = 'You are a helpful speech-to-text transcription assistant, always remaining factual and never hallucinating. You always provide an accurate answer for the task at hand, whether the procedure is completed succesfully or otherwise.',
    context_schema = Context,
    response_format = ResponseFormat,
    checkpointer = checkpointer
)

config = {'configurable': {'thread_id': '1'}}

response = agent.invoke({
    'messages': [
        {'role': 'user', 'content': "Get the stt and print the transcription of the file at audio/1Guslive.mp3."}
    ]},
    config = config,
    context = Context(user_id='B2', speech='LRE-Aniversario')
)

print('---------------------------------')
#print(response['messages'][-1].content)
print(response)
#print(response['structured_response'])
print('---------------------------------')
