from pydantic import BaseModel


class UserInput(BaseModel):
    request: str


class ApiKeyInput(BaseModel):
    api_key: str
    provider: str
