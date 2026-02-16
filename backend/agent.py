from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from backend.config import GROQ_API_KEY
from backend.custom_tools.tickets import view_tickets, create_ticket, update_ticket
# from backend.tools.customers import view_customers, create_customer
# from backend.tools.stats import ticket_stats  

llm = ChatGoogleGenerativeAI(
    model="qwen/qwen3-32b",
    google_api_key=GROQ_API_KEY,
    temperature=0
)

tools = [
    view_tickets,
    create_ticket,
    update_ticket,
    # view_customers,
    # create_customer,
    # ticket_stats
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)