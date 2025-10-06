from pydantic_core import ValidationError

from src.agents import AnswerAgent
from src.schemas import JSONOutput
from src.settings import settings
from src.utils.exceptions import ModelNotFoundException

MODELS = [
    'qwen/qwen3-32b',
    'llama-3.1-8b-instant',
    'llama-3.3-70b-versatile',
    'openai/gpt-oss-20b',
    'openai/gpt-oss-120b',
    'gemini-2.5-flash',
    'gemini-2.5-pro',
]


class Chat:
    """
    Represents the chat service that interacts with the AnswerAgent.
    This class should be managed as a singleton to maintain chat history.
    """

    def __init__(self, agent: AnswerAgent):
        # Recebe uma instância do agente em vez de criar uma nova.
        self.agent = agent

    async def send_prompt(self, user_input: str):
        response = self.agent.run(user_input)

        content = response['output'].replace('`', '').replace('json', '', 1)

        # Tentar converter em JSON, algumas respostas não são geradas no formato certo.
        try:
            response = JSONOutput.model_validate_json(content)
        except ValidationError:
            response = {'response': content, 'graph_id': ''}

        return response

    async def change_model(self, provider: str, model_name: str):
        if model_name not in MODELS:
            raise ModelNotFoundException(
                'Wrong model name received, try again with a valid model.'
            )

        if provider == 'google':
            self.agent.init_gemini_model(model_name=model_name, temperature=0)
        elif provider == 'groq':
            self.agent.init_groq_model(model_name=model_name, temperature=0)
        else:
            raise ModelNotFoundException('No provider found for the data received.')

        self.agent.initialize_agent(
            memory_key='chat_history', tools=self.agent.tools, prompt=self.agent.prompt
        )

        return {'detail': f'Model changed to {model_name} from {provider.upper()}'}


# --- Implementação do Singleton ---

_chat_instance: Chat | None = None


def get_chat_service(force_recreate: bool = False) -> Chat | None:
    """
    Returns a singleton instance of the Chat service.
    This ensures that the same agent and memory are used across requests.
    """
    global _chat_instance
    if _chat_instance is None or force_recreate:
        if settings.gemini_api_key or settings.groq_api_key:
            agent = AnswerAgent()
            _chat_instance = Chat(agent)

        else:
            return None

    return _chat_instance
