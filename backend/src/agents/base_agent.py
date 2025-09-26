from typing import Optional

from langchain.agents import AgentExecutor, Tool, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import BaseTool
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_core.language_models import BaseChatModel
from langchain_experimental.tools import PythonAstREPLTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from src.settings import settings


class BaseAgent:
    def __init__(
        self,
        llm: Optional[BaseChatModel] = None,
    ):
        self.__llm = llm
        self.executor = None
        self.prompt = ChatPromptTemplate(
            [
                ('system', 'You are a helpful agent that answers questions,'),
                (
                    'system',
                    'respond to the questions objectively and only when certain,',
                ),
                ('system', 'use the tools available to create better answers'),
                ('human', '{question}'),
                MessagesPlaceholder('agent_scratchpad'),
            ]
        )

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
            )
        ]
        return tools

    def init_gemini_model(self, model_name='gemini-2.5-flash', **kwargs) -> None:
        """Instantiate a Gemini chat model and register for the agent.

        Args:
            model_name (str, optional): Name of model to be used. Defaults to 'gemini-2.5-flash'.
            temperature (int, optional): Temperature used in the model.

        Raises:
            RuntimeError: raised when no API key is present.
        """
        if settings.gemini_api_key:
            self.__llm = ChatGoogleGenerativeAI(
                model_name=model_name, api_key=settings.gemini_api_key, **kwargs
            )

            return

        raise RuntimeError(
            'Your Gemini API key is null, add an API key to the environment to proceed.'
        )

    def init_groq_model(self, model_name='llama-3.1-8b-instant', **kwargs) -> None:
        """Instantiate a Groq chat model and register for the agent.

        Args:
            model_name (str, optional): Name of model to be used. Defaults to 'llama-3.1-8b-instant'.
            temperature (int, optional): Temperature used in the model

        Raises:
            RuntimeError: raised when no API key is present.
        """
        if settings.groq_api_key:
            self.__llm = ChatGroq(
                model_name=model_name, api_key=settings.groq_api_key, **kwargs
            )

            return

        raise RuntimeError(
            'Your Groq API key is null, add an API key to the environment to proceed.'
        )

    def initialize_agent(
        self, tools: list[BaseTool] = None, prompt: ChatPromptTemplate | None = None
    ):
        """Instantiate an agent using the defined options.

        Args:
            tools (any, optional): Tools for the agent, if None the default toolset is used.
            prompt (ChatPromptTemplate | None, optional): Prompt template used in the agent, if None the default template is used.

        Raises:
            RuntimeError: if no LLM is instantiated before using the agent
        """
        if not self.__llm:
            raise RuntimeError(
                'No llm found, instantiate a model first with the available methods.'
            )

        agent = create_tool_calling_agent(
            self.__llm, tools=tools or self.tools, prompt=prompt or self.prompt
        )
        self.executor = AgentExecutor(agent=agent, tools=tools or self.tools)

    def run(self, question: str):
        if not self.executor:
            raise RuntimeError(
                'No agent found, initialize the agent first with initialize_agent method.'
            )

        return self.executor.invoke({'question': question})
