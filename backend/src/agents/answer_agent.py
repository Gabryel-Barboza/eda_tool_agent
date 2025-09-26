from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool
from langchain_experimental.tools import PythonAstREPLTool

from src.tools.datetime_tool import get_current_datetime
from src.tools.sql_agent_tool import use_sql_agent
from src.utils.exceptions import ModelNotFoundException

from .base_agent import BaseAgent


class AnswerAgent(BaseAgent):
    def __init__(self):
        prompt_model = ChatPromptTemplate(
            [
                (
                    'system',
                    'You are a helpful assistant that answers users questions objectively. Follow the rules:',
                ),
                (
                    'system',
                    '* use your tools available when necessary to improve your response',
                ),
                (
                    'system',
                    '* only answer if you have the knowledge, otherwise do not invent information.',
                ),
                (
                    'system',
                    '* use the SQL tool for answering questions about the database, such as:',
                ),
                ('system', '  * How many registries are there for the sales table?'),
                ('system', '  * Return the mean of the salary of employees'),
                (
                    'system',
                    '  * Get the total of sales that occurred between 01/2025 and 04/2025.',
                ),
                (
                    'system',
                    '* first, identify the database scope and then generate matching questions.',
                ),
                ('human', '{question}'),
                MessagesPlaceholder('agent_scratchpad'),
            ]
        )

        super().__init__()

        # Agent configuration
        self.init_groq_model()
        self.initialize_agent(tools=self.tools, prompt=prompt_model)

    @property
    def tools(self):
        """Add tools to amplify the agent capabilities."""
        if not self._llm:
            raise ModelNotFoundException

        tools = [
            get_current_datetime,
            use_sql_agent,
            Tool(
                name='Python Code',
                func=PythonAstREPLTool,
                description='Use this tool to code and for answering complex questions that require calculations or data manipulation. Use the pandas lib when required for data manipulation or graphical visualization.',
            ),
        ]

        return tools
