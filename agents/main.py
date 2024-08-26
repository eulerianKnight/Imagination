import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from models import UserConfiguration, UserQuery
from agent import Agent
import redis

load_dotenv()

app = FastAPI()

# Dictionary to store generated endpoints
endpoints = {}

@app.post("/generate_endpoint")
def generate_endpoint(user_config: UserConfiguration):
    # Generate a unique endpoint base path
    endpoint_base = f"/user/{user_config.USERNAME}"

    # Create endpoints for Chat dynamically
    @app.post(f"{endpoint_base}/chat")
    async def chat(request: UserQuery):
        # agent = Agent(config=user_config)
        # react_agent = agent.create_react_agent()
        return {"message": "POST data received"}

    @app.get(f"{endpoint_base}/info")
    async def user_get_endpoint():
        # Implement GET logic for the user
        return {"user_info": user_config.dict()}

    # Store the endpoints in the dictionary
    endpoints[endpoint_base] = {
        "post": chat,
        "get": user_get_endpoint
    }

    return {"endpoints": {
        "post": f"{endpoint_base}/data",
        "get": f"{endpoint_base}/info"
    }}