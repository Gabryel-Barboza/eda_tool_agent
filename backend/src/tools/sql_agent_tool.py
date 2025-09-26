from langchain.tools import tool

from src.agents.sql_agent import SQLAgent
from src.tools.database_tool import db


@tool('SQL Specialist')
def use_sql_agent(query: str):
    """This is a tool used to create and execute SQL scripts in a pre-created database based on a user query received. The result of the query executed is returned."""
    agent = SQLAgent()
    response = agent.run(query, db.dialect)

    return {'result': response.output}
