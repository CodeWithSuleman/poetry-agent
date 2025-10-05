from fastapi import FastAPI
from pydantic import BaseModel
from agents import Runner, SQLiteSession
from connection import config
from main import poetry_agent
from fastapi.middleware.cors import CORSMiddleware

class Message(BaseModel):
    message: str

session = SQLiteSession("poetry_agent.db")

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://poetry-assistant-aazs.vercel.app/"], 
    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Message):
    user_input = request.message.strip()
    if not user_input:
        return {"response": "Please provide a valid message."}

    result = await Runner.run(
        poetry_agent, 
        input=user_input, 
        run_config=config,
        session=session,
        )
    return {"response": result.final_output or "Sorry, I couldn't compose that."}
