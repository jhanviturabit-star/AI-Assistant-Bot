# from fastapi import FastAPI, Header
# from pydantic import BaseModel
# from langchain_openai import ChatOpenAI
# from langchain.agents import initialize_agent, AgentType

# from tools.tickets import get_all_tickets, create_ticket
# from tools.customers import get_all_customers, create_customer
# from tools.stats import get_ticket_stats
# from config import GROK_API_KEY  

# app = FastAPI()

# llm = ChatOpenAI(
#     model="qwen/qwen3-32b",
#     api_key=GROK_API_KEY, 
#     base_url="https://api.groq.com/openai/v1",
#     temperature=0
# )

# tools = [get_all_tickets, create_ticket, get_all_customers, create_customer, get_ticket_stats]

# agent = initialize_agent(
#     tools=tools,
#     llm=llm,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True
# )

# class ChatRequest(BaseModel):
#     message: str

# @app.post("/chat")
# async def chat(request: ChatRequest, authorization: str = Header(None)):
#     if not authorization:
#         return {"error": "Authorization header missing. Please log in first."}

#     response = agent.run({
#         "input": request.message,
#         "token": authorization  # dynamically forward JWT
#     })

#     return {"response": response}

from fastapi.security import HTTPBearer
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.tools import tool

from .custom_tools import *
from backend.auth import auth_router
from backend.config import GROK_API_KEY
from backend.context import current_token

app = FastAPI(title="CRM AI Assistant")

app.include_router(auth_router)

# ---------------------
# LLM Setup
# ---------------------
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=GROK_API_KEY,
    temperature=0
)

# ---------------------
# Tools Setup
# ---------------------
tools = [create_customer, create_ticket, get_all_customers, get_all_tickets, get_filtered_tickets, get_ticket_summary, update_ticket_status]
# tools = [
#     Too(
#         name_or_callable="Get_All_Tickets"
#     )
#     # tool(
#     #     name_or_callable="Create_Ticket",
#     #     description="Create a new ticket. Input should be ticket details"
#     # ),
#     # tool(
#     #     name_or_callable="Get_All_Customers",
#     #     description="Retrieve all customers from the system"
#     # ),
#     # tool(
#     #     name_or_callable="Create_Customer",
#     #     description="Create a new customer. Input should be customer details"
#     # )
#     # tool(
#     #     name="Get_Ticket_Stats",
#     #     func=get_ticket_stats,
#     #     description="Retrieve ticket statistics and analytics"
#     # ),
# ]

# ---------------------
# Agent Setup
# ---------------------

prompt = """
You are a CRM agent assistant. You can have the tools {tools} for performing actions.
"""

# Create the agent
agent = create_agent(llm, tools=tools, system_prompt=prompt)

# Create the agent executor
# agent_executor = AgentExecutor(
#     agent=agent,
#     tools=tools,
#     verbose=True,
#     handle_parsing_errors=True
# )

# ---------------------
# Request Model
# ---------------------
class ChatRequest(BaseModel):
    message: str

# ---------------------
# Chat Endpoint
# ---------------------
security =  HTTPBearer()

@app.post("/chat")
async def chat(request: ChatRequest, credentials = Depends(security)):
    """chat API"""

    raw_token = credentials.credentials

    print("RAW credentials.credentials:", raw_token)

    if raw_token and raw_token.startswith("Bearer "):
        raw_token = raw_token.replace("Bearer ", "")

    current_token.set(raw_token)

    try:
        response = agent.invoke({
            "messages": [
                {"role": "user", "content": request.message}
            ]
        })
        return {"response": response["messages"][-1].content}


    except Exception as e:
        return {"error": str(e)}

# ---------------------
# Root Endpoint
# ---------------------
@app.get("/")
async def root():
    """/"""
    return {"message": "CRM AI Assistant is running."}