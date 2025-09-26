from langchain.tools import tool
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langchain_community.utilities import SQLDatabase

from src.settings import settings

DATABASE_URI = settings.database_uri

db = SQLDatabase.from_uri(DATABASE_URI)


@tool('Execute Query')
def execute_query(query: str):
    """Tool for executing SQL Query passed as a parameter."""
    query_tool = QuerySQLDatabaseTool(db=db)
    response = query_tool.invoke(query)

    return {'result': response}
