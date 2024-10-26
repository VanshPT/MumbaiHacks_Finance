# blijax.py
import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain.agents import initialize_agent, Tool
from langchain_community.utilities import SerpAPIWrapper
import requests
import json
from QA.qa import urlSummarizer

# Load environment variables
load_dotenv()

# Function to generate responses using the local Llama model
def generate_with_llama(prompt):
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "llama2",
        "prompt": prompt
    }
    
    response_content = ""
    
    with requests.post(url, json=payload, stream=True) as response:
        for line in response.iter_lines():
            if line:
                line_str = line.decode("utf-8")
                try:
                    line_json = json.loads(line_str)
                    response_content += line_json.get("response", "")
                    if line_json.get("done", False):
                        break
                except json.JSONDecodeError:
                    continue
    return response_content

class Blijax:
    def __init__(self, model="llama2", response_format="in 5 sentences"):
        # Initialize your class variables and agent here
        self.model = model
        self.response_format = response_format
        self.agent = None  # Replace with actual agent initialization

    def setUpChain(self, functionList):
        """
        Set up the decision chain using the provided function list.
        """
        # Example of setting up a chain (replace with your actual logic)
        self.decision_chain = initialize_agent(functionList, self.agent, verbose=True)
        print("Decision chain set up successfully.")

    def questionsAboutCurrent(self, input) -> str:
        """
        Good for checking questions about current events, weather updates, or things similar.
        """
        return self.agent.run(input)

    def generalConversation(self, input) -> str:
        return generate_with_llama(f"You are Blijax, an assistant who helps answer stock market-related questions. Respond accordingly to this input: {input}. Sometimes use emojis to express your emotions.")
    
    # Generates Response
    def generate(self, text):
        input = text
        decision = self.decision_chain.run(input)
        print(decision)
        
        if decision["name"] == "retrieveNews":
            newsReply = self.retrieveNews(decision["arguments"]["company_name"])
            newsReply = "".join(newsReply)
            return newsReply
        
        elif decision["name"] == "retrieveStocks":
            ticker = self.retrieveTicker(input)
            print(ticker["ticker"])
            tickerReply = self.retrieveStocks(ticker["ticker"], input)
            return generate_with_llama(f"Can you summarize this?: {tickerReply}") 
        
        elif decision["name"] == "questionsAboutCurrent":
            return self.questionsAboutCurrent(input)
        
        elif decision["name"] == "generalConversation":
            return self.generalConversation(input)
