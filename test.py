# from langchain_openai import ChatOpenAI

# llm = ChatOpenAI(
#     model="qwen/qwen3-32b",
#     api_key="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",
#     base_url="https://api.groq.com/openai/v1",
#     temperature=0
# )

# response = llm.invoke("Say hello in one sentence.")
# print(response.content)


import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

llm = ChatGroq(
    model_name="qwen/qwen3-32b", 
    groq_api_key="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",
    temperature=0.7
)


messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="I am diyaa")
]

response = llm.invoke(messages)

print(response.content)