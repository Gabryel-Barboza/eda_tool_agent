from src.agents.sql_agent import SQLAgent


# SQL function tool
def use_sql_agent(query: str):
    agent = SQLAgent()
    response = agent.run(query)

    return response.output
