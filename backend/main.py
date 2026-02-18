from fastapi.security import HTTPBearer
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain.agents import create_agent
#from langchain.tools import tool

from .custom_tools import *
from backend.auth import auth_router
from backend.config import GROQ_API_KEY
from backend.context import current_token
from backend.routes import tickets, customers
from backend.auth import get_current_user

app = FastAPI(title="CRM AI Assistant")

app.include_router(auth_router)
app.include_router(tickets.router)
app.include_router(customers.router)


# ---------------------
# LLM Setup
# ---------------------
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=GROQ_API_KEY,
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
You are a CRM agent assistant. 
IMPORTANT RULES:
- Use tools for CRM operations.
- Call a tool only once per user request.
- After receiving the tool result, respond to the user.
- Do NOT call the same tool multiple times for the same request.
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
async def chat(request: ChatRequest, user=Depends(get_current_user)):
    """chat API"""

    current_token.set(user["token"])

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