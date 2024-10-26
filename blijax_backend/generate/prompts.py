# prompts.py
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

# Define your prompts here

# Example prompt template
prompt_template = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a helpful assistant."),
    HumanMessagePromptTemplate.from_template("What is the weather like in {location}?"),
])

def get_weather_prompt(location):
    return prompt_template.format_messages(location=location)
