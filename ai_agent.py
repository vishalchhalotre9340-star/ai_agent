



# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# from langchain_groq import ChatGroq 
# from langchain_openai import ChatOpenAI
# from langchain_tavily import TavilySearch 
# from langchain_core.messages import AIMessage, HumanMessage 
# from langchain.agents import create_agent

# # System prompt
# system_prompt = "Act as an AI chatbot who is smart and friendly"

# # ✅ Main function
# def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    
#     # 🔹 Select LLM
#     if provider.lower() == "groq":
#         llm = ChatGroq(
#             model=llm_id,
#             api_key=GROQ_API_KEY
#         )
        
#     elif provider.lower() == "openai":
#         llm = ChatOpenAI(
#             model=llm_id,
#             api_key=OPENAI_API_KEY
#         )
#     else:
#         raise ValueError("Invalid provider ❌")

#     # 🔹 Tools (FIXED ✅)
#     if allow_search:
#         if not TAVILY_API_KEY:
#             raise ValueError("TAVILY_API_KEY missing ❌")
        
#         tools = [
#             TavilySearch(
#                 max_results=2,
#                 tavily_api_key=TAVILY_API_KEY
#             )
#         ]
#     else:
#         tools = []

#     # 🔹 Create Agent (FIXED ✅ llm use)
#     agent = create_agent(
#         model=llm,
#         tools=tools,
#         system_prompt=system_prompt
#     )

#     # 🔹 Invoke
#     state = {
#         "messages": [HumanMessage(content=query)]
#     }

#     response = agent.invoke(state)

#     # 🔹 Extract AI message
#     messages = response.get("messages", [])
#     ai_messages = [
#         message.content for message in messages 
#         if isinstance(message, AIMessage)
#     ]

#     return ai_messages[-1] if ai_messages else "No response"





import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ Updated imports
from langchain_groq import ChatGroq 
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import AIMessage, HumanMessage 
from langchain.agents import create_agent

# System prompt
system_prompt = "Act as an AI chatbot who is smart and friendly"

# ✅ Main function
def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    
    # 🔹 Select LLM
    if provider.lower() == "groq":
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY missing ❌")
            
        llm = ChatGroq(
            model=llm_id,
            api_key=GROQ_API_KEY
        )
        
    elif provider.lower() == "openai":
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY missing ❌")
            
        llm = ChatOpenAI(
            model=llm_id,
            api_key=OPENAI_API_KEY
        )
    else:
        raise ValueError("Invalid provider ❌")

    # 🔹 Tools (UPDATED ✅)
    if allow_search:
        if not TAVILY_API_KEY:
            raise ValueError("TAVILY_API_KEY missing ❌")
        
        tools = [
            TavilySearchResults(
                max_results=2,
                tavily_api_key=TAVILY_API_KEY
            )
        ]
    else:
        tools = []

    # 🔹 Create Agent
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt
    )

    # 🔹 Invoke agent
    state = {
        "messages": [HumanMessage(content=query)]
    }

    response = agent.invoke(state)

    # 🔹 Extract AI message
    messages = response.get("messages", [])
    ai_messages = [
        message.content for message in messages 
        if isinstance(message, AIMessage)
    ]

    return ai_messages[-1] if ai_messages else "No response"












