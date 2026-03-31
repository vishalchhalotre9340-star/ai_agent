
    
    
    
# from typing import List
# from pydantic import BaseModel
# from fastapi import FastAPI
# from ai_agent import get_response_from_ai_agent

# # ✅ Pydantic model (separate)
# class RequestState(BaseModel):
#     model_name: str
#     model_provider: str
#     system_prompt: str
#     messages: List[str]
#     allow_search: bool

# # ✅ FastAPI app
# app = FastAPI(title="LangGraph AI Agent")

# ALLOWED_MODELS = [
#     "llama3-70b-8192",
#     "mixtral-8x7b-32768",
#     "llama-3.3-70b-versatile",
#     "gpt-4o-mini"
# ]

# # ✅ API endpoint
# @app.post("/chat")
# def chat(request: RequestState):
#     if request.model_name not in ALLOWED_MODELS:
#         return {"error": "Invalid model name. Kindly choose from allowed models."}
    
#     response= get_response_from_ai_agent(
#         llm_id=request.model_name,
#         query=request.messages[-1],
#         allow_search=request.allow_search,
#         system_prompt=request.system_prompt,
#         provider=request.model_provider   )
#     return response
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)





from typing import List
from pydantic import BaseModel
from fastapi import FastAPI
from ai_agent import get_response_from_ai_agent

# ✅ Pydantic model
class RequestState(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[str]
    allow_search: bool

# ✅ FastAPI app
app = FastAPI(title="LangGraph AI Agent")

ALLOWED_MODELS = [
    "llama3-70b-8192",
    "mixtral-8x7b-32768",
    "llama-3.3-70b-versatile",
    "gpt-4o-mini"
]

# ✅ API endpoint
@app.post("/chat")
def chat(request: RequestState):
    if request.model_name not in ALLOWED_MODELS:
        return {"error": "Invalid model name. Kindly choose from allowed models."}
    
    response = get_response_from_ai_agent(
        llm_id=request.model_name,
        query=request.messages[-1],
        allow_search=request.allow_search,
        system_prompt=request.system_prompt,
        provider=request.model_provider
    )
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)