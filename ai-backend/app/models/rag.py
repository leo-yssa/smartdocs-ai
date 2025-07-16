from pydantic import BaseModel

class SearchRequest(BaseModel):
    query: str

class SearchResponse(BaseModel):
    results: list

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str 