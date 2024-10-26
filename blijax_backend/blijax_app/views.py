from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Text
from generate.generate import Blijax
import random

# Define your functions for the decision chain

def retrieveNews(company_name: str) -> str:
    # Dummy implementation to simulate news retrieval
    news_samples = [
        f"{company_name} has launched a new product!",
        f"{company_name} stocks have risen by 5% this week.",
        f"{company_name} announced a partnership with another tech firm.",
        f"{company_name} faces regulatory scrutiny over recent practices.",
        f"{company_name} achieved record sales this quarter."
    ]
    return random.choice(news_samples)

def retrieveStocks(company_name: str) -> str:
    # Dummy implementation to simulate stock information retrieval
    stock_price = round(random.uniform(100, 500), 2)
    return f"The current stock price of {company_name} is ${stock_price}."

def questionsAboutCurrent(input: str) -> str:
    # Dummy implementation for current events questions
    return f"You asked about: {input}. It's an interesting topic!"

def generalConversation(input: str) -> str:
    # Dummy implementation for general conversation
    return f"Let's talk about {input}. What do you want to know?"

# Define the function list for your decision chain
functionList = [retrieveNews, retrieveStocks, generalConversation]

# Initialize the Blijax model and set up the chain
blijax_model = Blijax("llama2", "in 5 sentences")  # Updated to use llama2
blijax_model.setUpChain(functionList)

# Handle POST requests to summarize the input text
@api_view(["POST"])
def summarize_view(request):
    # Handle data inputs
    if request.method == "POST":
        # Get the data and provide None if not given
        text = request.data.get("text", None)

        # Add it to the database and save
        new_addition = Text(text=text)
        new_addition.save()

        # Pull the text and summarize it
        try: 
            summary = blijax_model.generate(new_addition.text)
        except Exception as e:
            print(e)
            summary = "Sorry, something went wrong. Please try again."

        # Return the answer & status 200 (meaning everything worked!)
        return Response(summary, status=200)

