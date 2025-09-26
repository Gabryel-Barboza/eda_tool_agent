from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing_extensions import Annotated, TypedDict

from src.tools.database_tool import execute_query
from src.utils.exceptions import ExecutorNotFoundException, ModelNotFoundException

from .base_agent import BaseAgent


class QueryOutput(TypedDict):
    query: Annotated[str, ..., 'Syntactically valid SQL query.']


class SQLAgent(BaseAgent):
    def __init__(self):
        prompt_model = ChatPromptTemplate(
            [
                (
                    'system',
                    'You are a SQL specialist focused in creating SQL scripts. Follow the rules:',
                ),
                (
                    'system',
                    '* use the tools available to execute the scripts you generate or to get info about the database.',
                ),
                (
                    'system',
                    '* you are not allowed to create, drop or access other databases.',
                ),
                (
                    'system',
                    '* you can create & drop tables, use DML or DQL statements.',
                ),
                (
                    'system',
                    '* pay attention to the tables & columns names when creating scripts, use only existing values in the tables.',
                ),
                (
                    'system',
                    '* never create scripts that return all registries from the database, always limit the results to 10 or more if specified.',
                ),
                (
                    'system',
                    '* The DBMS used is {dialect}, use his syntax when creating scripts',
                ),
                ('human', '{query}'),
                ('human', '{data}'),
                MessagesPlaceholder('agent_scratchpad'),
            ]
        )

        # Agent configuration
        self.init_groq_model(temperature=0)
        self.add_output_parser(QueryOutput)
        self.initialize_agent(tools=self.tools, prompt=prompt_model)

    @property
    def tools(self):
        if not self._llm:
            raise ModelNotFoundException()
        return [execute_query]

    def run(self, query: str, dialect: str, data: any | None = None):
        if not self.executor:
            raise ExecutorNotFoundException()

        return self.executor.invoke({'query': query, 'dialect': dialect, 'data': data})
