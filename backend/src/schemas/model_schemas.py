from pydantic import BaseModel, Field


class JSONOutput(BaseModel):
    response: str = Field(description='Model answer.')
    graph: str = Field(description='plotly graph returned if required.')


class QueryOutput(BaseModel):
    query: str = Field(description='Syntactically valid SQL query.')
