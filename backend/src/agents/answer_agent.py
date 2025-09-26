from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_experimental.tools import PythonAstREPLTool

from src.tools.sql_agent_tool import use_sql_agent

from .base_agent import BaseAgent


class AnswerAgent(BaseAgent):
    def __init__(self):
        prompt_model = ChatPromptTemplate(
            [
                (
                    'system',
                    '',
                ),
                ('human', '{question}'),
                MessagesPlaceholder('agent_scratchpad'),
            ]
        )

        super().__init__()

        # Agent configuration
        self.init_groq_model(temperature=0)
        self.initialize_agent(tools=self.tools, prompt=prompt_model)

    @property
    def tools(self):
        """Add tools to amplify the agent capabilities."""
        if not self.__llm:
            raise RuntimeError(
                'No llm found, instantiate a model first with the available methods.'
            )

        tools = load_tools(['llm-math'], llm=self.__llm) + [
            Tool(
                name='Python Code',
                func=PythonAstREPLTool,
                description='Use this tool to code and for answering complex questions that require calculations or data manipulation. Use the pandas lib when required for data manipulation.',
            ),
            Tool(
                'SQL Specialist',
                func=use_sql_agent,
                description='This is a tool used to create and execute SQL scripts in a pre-created database based on a query received. The result of the query executed is returned.',
            ),
        ]
        return tools
