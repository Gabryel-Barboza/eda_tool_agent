from typing import Optional

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import BaseTool
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from src.settings import settings
from src.utils.exceptions import (
    APIKeyNotFoundException,
    ExecutorNotFoundException,
    ModelNotFoundException,
)


class BaseAgent:
    def __init__(
        self,
        llm: Optional[BaseChatModel] = None,
    ):
        self._llm = llm
        self.executor = None
        self.prompt = ChatPromptTemplate(
            [
                ('system', 'You are a helpful agent that answers questions,'),
                (
                    'system',
                    'respond to the questions objectively and only when certain,',
                ),
                ('system', 'use the tools available to create better answers'),
                ('system', '{format_instructions}'),
                ('human', '{input}'),
                MessagesPlaceholder('agent_scratchpad'),
            ]
        )

    @property
    def tools(self):
        """Add tools to amplify the agent capabilities."""
        if not self._llm:
            raise ModelNotFoundException()

        tools = []

        return tools

    def init_gemini_model(self, model_name='gemini-1.5-pro', **kwargs) -> None:
        """Instantiate a Gemini chat model and register for the agent.

        Args:
            model_name (str, optional): Name of model to be used. Defaults to 'gemini-1.5-pro'.
            temperature (int, optional): Temperature used in the model.

        Raises:
            APIKeyNotFoundException: raised when no API key is present.
        """
        if settings.gemini_api_key:
            self._llm = ChatGoogleGenerativeAI(
                model=model_name, api_key=settings.gemini_api_key, **kwargs
            )
            self.model_name, self.provider = model_name, 'google'

            return

        raise APIKeyNotFoundException(
            'Your Gemini API key is null, add an API key to the environment to proceed.'
        )

    def init_groq_model(self, model_name='qwen/qwen3-32b', **kwargs) -> None:
        """Instantiate a Groq chat model and register for the agent.

        Args:
            model_name (str, optional): Name of model to be used. Defaults to 'qwen/qwen3-32b'.
            temperature (int, optional): Temperature used in the model

        Raises:
            APIKeyNotFoundException: raised when no API key is present.
        """
        if settings.groq_api_key:
            self._llm = ChatGroq(
                model_name=model_name, api_key=settings.groq_api_key, **kwargs
            )
            self.model_name, self.provider = model_name, 'groq'

            return

        raise APIKeyNotFoundException(
            'Your Groq API key is null, add an API key to the environment to proceed.'
        )

    def initialize_agent(
        self,
        memory_key: str = None,
        memory: ConversationBufferWindowMemory = None,
        tools: list[BaseTool] = None,
        prompt: ChatPromptTemplate | None = None,
        verbose: bool = True,
    ):
        """Instantiate an agent using the defined options. Should be used after modifying the LLM object.

        Args:
            tools (any, optional): Tools for the agent, if None the default toolset is used.
            prompt (ChatPromptTemplate | None, optional): Prompt template used in the agent, if None the default template is used.

        Raises:
            ModelNotFoundException: if no LLM is instantiated before using the agent.
        """
        if not self._llm:
            raise ModelNotFoundException()

        agent = create_tool_calling_agent(
            self._llm, tools=tools or self.tools, prompt=prompt or self.prompt
        )

        if memory_key:
            memory = ConversationBufferWindowMemory(
                memory_key=memory_key,
                k=5,
                input_key='input',
                output_key='output',
                return_messages=True,
            )

        self.executor = AgentExecutor(
            agent=agent,
            tools=tools or self.tools,
            memory=memory,
            max_iterations=7,
            verbose=verbose,
        )

    def run(self, user_input: str, output_instructions: str | None = None):
        if not self.executor:
            raise ExecutorNotFoundException()

        return self.executor.invoke(
            {'input': user_input, 'format_instructions': output_instructions}
        )

    def get_model_info(self):
        return (self.model_name, self.provider)

    def get_json_parser(self, output_model: any):
        """Create a structured JSON output parser for the model response.

        Args:
            output_model (any): A BaseModel class with the output format for JSON.
        Returns:
            instructions (str): Parser instructions for use in model prompt.
        """
        parser = JsonOutputParser(pydantic_object=output_model)
        instructions = parser.get_format_instructions()

        return instructions
