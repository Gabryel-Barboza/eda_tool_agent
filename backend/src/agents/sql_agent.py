from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase

from src.settings import settings
from src.utils.exceptions import ExecutorNotFoundException, ModelNotFoundException

from .base_agent import BaseAgent

DATABASE_URI = settings.database_uri
db = SQLDatabase.from_uri(DATABASE_URI)


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
                    '* you are allowed to create & drop tables, and use DML or DQL statements.',
                ),
                (
                    'system',
                    '* pay attention to the tables & columns names when creating scripts, use only existing values in the tables.',
                ),
                (
                    'system',
                    '* never create scripts that return all registries from the database, always limit the results between 10 and 100.',
                ),
                (
                    'system',
                    '* The DBMS used is {dialect}, use his syntax when creating scripts',
                ),
                ('system', '* Your response must be one of:'),
                ('system', '  * [SQL query results]'),
                ('system', '  * the string "no data found" if empty.'),
                ('human', '{query}'),
                ('human', '{data}'),
                MessagesPlaceholder('agent_scratchpad'),
            ]
        )

        # Agent configuration
        self.init_groq_model('openai/gpt-oss-120b', temperature=0)
        self.initialize_agent(tools=self.tools, prompt=prompt_model)

    @property
    def tools(self):
        if not self._llm:
            raise ModelNotFoundException()

        toolkit = SQLDatabaseToolkit(db=db, llm=self._llm)
        tools = toolkit.get_tools()

        return tools

    def run(self, query: str, data=None):
        if not self.executor:
            raise ExecutorNotFoundException()

        return self.executor.invoke(
            {'query': query, 'dialect': db.dialect, 'data': data}
        )
