from langchain.tools import tool
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase

from src.settings import settings

DATABASE_URI = settings.database_uri
DATABASE_NAME = settings.database_name

db = SQLDatabase.from_uri(DATABASE_URI)


@tool('Get_tables')
def get_tables():
    """Tool for returning all tables from database. Doesn't work with SQLite, use SQL for that!"""
    query_tool = QuerySQLDatabaseTool(db=db)
    query = f"SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_schema = '{DATABASE_NAME}' AND table_type = 'BASE TABLE';"

    response = query_tool.invoke(query)

    return {'result': response}


@tool('Execute_query')
def execute_query(query: str):
    """Tool for executing SQL Query passed as a parameter."""
    query_tool = QuerySQLDatabaseTool(db=db)
    response = query_tool.invoke(query)

    return {'result': response}
