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
                    '* use your tools available when necessary',
                ),
                (
                    'system',
                    '* only answer if you have the knowledge, otherwise do not invent information.',
                ),
                (
                    'system',
                    '* When needed, use the SQL Specialist to answer specific questions with the database data, providing it with detailed user request, such as:',
                ),
                ('system', '  * Return the mean salary of employees'),
                (
                    'system',
                    '  * Get the total of sales that occurred between 01/2025 and 04/2025.',
                ),
                ('system', '  * What tables are present in the database?'),
                ('system', '* No SQL is passed to this tool, only requests for data.'),
                (
                    'system',
                    '* generate graphs representing the data for the user using "plotly", only when the user requires, return empty strings otherwise.',
                ),
                ('system', '{format_instructions}'),
                ('human', '{input}'),
                MessagesPlaceholder('agent_scratchpad'),
            ]
        )

        # Agent configuration
        self.prompt = prompt_model
        self.init_groq_model(temperature=0)
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
                name='Python_code',
                func=PythonAstREPLTool(),
                description='Tool for executing code. Use this for efficiency in complex or math tasks, "plotly" is available for graph creation.',
            ),
        ]

        return tools
