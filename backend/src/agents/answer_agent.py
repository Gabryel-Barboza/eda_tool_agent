from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool
from langchain_core.messages import SystemMessage
from langchain_experimental.tools import PythonAstREPLTool

from src.tools.datetime_tool import get_current_datetime
from src.tools.parser_tool import json_output_parser
from src.tools.sql_agent_tool import use_sql_agent
from src.utils.exceptions import ModelNotFoundException

from .base_agent import BaseAgent


class AnswerAgent(BaseAgent):
    def __init__(self):
        system_instructions = """You are a helpful assistant that answers users questions objectively. Follow the rules:
    * use your tools available when necessary 
    * use the user's language for response. 
    * use emojis in your response.
    * do not invent information.
    * When needed, use the SQL Specialist to answer specific questions with the database data, providing it with detailed user request, such as: 
        * Return the mean salary of employees .
        * Get the total of sales that occurred between 01/2025 and 04/2025. 
        * What tables are present in the database? 
        * No SQL is passed to this tool, only requests for data. 
    * generate graphs representing the data for the user using 'plotly', only when the user requires, return empty strings otherwise. Follow rules for graphs:
        * always export plotly graphs using to_dict method.
    * Your output should follow the JSON schema:
        {"response": "...", "graph": ""}
    * the JSON output format can be generated using the JSON_parser tool. Use this to finish the user request if necessary."""

        prompt_model = ChatPromptTemplate(
            [
                SystemMessage(system_instructions),
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
            json_output_parser,
            use_sql_agent,
            Tool(
                name='Python_code',
                func=PythonAstREPLTool(),
                description='Tool for executing code. Do not use this tool for printing code. Use this for efficiency in math or complex tasks, "plotly" is available for graph creation.',
            ),
        ]

        return tools
