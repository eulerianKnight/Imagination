from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class UserInfo(BaseModel):
    username: str
    email: str
    password: str
    role: str

class Token(BaseModel):
    username: str
    access_token: str
    token_type: str

class UserConfiguration(BaseModel):
    USERNAME: str
    AGENT_NAME: str
    SYSTEM_MESSAGE: str
    TOOLS: List[str]
    MODEL: str
    TEMPERATURE: Optional[float]
    PRESENCE_PENALTY: Optional[float]
    FREQUENCY_PENALTY: Optional[float]
    TOP_P: Optional[float]
    MAX_TOKENS: Optional[int]

class UserQuery(BaseModel):
    username: str
    query: str


class VectorSearch(BaseModel):
    collections: str = Field("Collection name to search in ChromaDB. Collection name is same as Username")