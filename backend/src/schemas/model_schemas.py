from pydantic import BaseModel, Field


class JSONOutput(BaseModel):
    response: str = Field(description='Model answer.')
    graph: str | None = Field(description='plotly lib graph if required.')


class QueryOutput(BaseModel):
    query: str = Field(description='Syntactically valid SQL query.')
