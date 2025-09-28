from langchain.tools import tool

from src.agents.sql_agent import SQLAgent


@tool('SQL_specialist')
def use_sql_agent(user_request: str):
    """This tool is used to create and execute SQL scripts in a database based on a user request received. This function input should be an instruction to generate the result expected from the user. The result of the query executed is returned."""
    agent = SQLAgent()
    response = agent.run(user_request)

    return {'result': response['output']}
