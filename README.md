# Coupon Code Retriever and Evaluator
## Project Overview
This project provides an AI-powered agent that can retrieve and evaluate discount coupon codes for retailers and products. It uses LangChain for handling the conversation and integrates with tools that fetch coupon codes and check their validity.

The system works in two main steps:

1. Crawling: It fetches coupon codes from multiple providers for a given retailer and product (optional).
2. Evaluating: It checks whether the retrieved coupon codes are valid or not and provides feedback to the user.

## How It Works
1. Tool Caller:

- Receives user input and determines if the system should fetch coupons or test already retrieved ones.
- Calls the get_coupons tool if a new request for coupons is made.
- Calls the try_coupons tool if the user wants to test existing coupon codes.

2. Coupon Tools:

- **get_coupons**: Simulates fetching coupon codes for a specified retailer and product from a randomly chosen coupon provider.
- **try_coupons**: Simulates testing the validity of each coupon code by randomly determining whether the code is valid or not.

3. Answer Generator:

- After the coupons are retrieved and evaluated, the system generates a response based on the results and presents it to the user.

# Configuration
## .env

Make sure to have a .env file containing your OpenAI API key:

Kodu kopyala
```python
OPENAI_API_KEY=your-openai-api-key
```

## config.py
This file holds the model names, system messages, and other configuration settings:

```python
TOOL_CALLER_MODEL_NAME = 'gpt-4o-mini'
ANSWER_GENERATOR_MODEL_NAME = 'gpt-3.5-turbo'
TOOL_CALLER_TEMPERATURE = 0
ANSWER_GENERATOR_TEMPERATURE = 0.3
TOOL_CALLER_SYSTEM_MESSAGE = """
    You are an AI agent whose job is to use a tool to find discount coupon codes or evaluate the validity of retrieved codes.
    """
ANSWER_GENERATOR_SYSTEM_MESSAGE = """
    You are an AI agent whose job is to generate an answer based on previous Tool and/or AI messages.
    """
```

## Example Flow
1. **User Input**: "I need a coupon code for electronics."
2. **Tool Call**: The system calls the get_coupons tool to fetch coupon codes.
3. **Coupon Retrieval**: A list of dummy coupon codes is generated for the retailer.
4. **User Prompt**: The system asks if the user would like to try any of the codes.
5. **Coupon Evaluation**: The system evaluates the validity of the coupon codes using the try_coupons tool.
6. **Response**: The system informs the user which codes are valid and whether they need to fetch more coupons.