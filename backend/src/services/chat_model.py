from pydantic_core import ValidationError

from src.agents import AnswerAgent
from src.schemas import JSONOutput
from src.utils.exceptions import ModelNotFoundException


class Chat:
    def __init__(self):
        # Init selected LLM model
        self.agent = AnswerAgent()
        # Init agent with llm
        self.agent.initialize_agent(
            memory_key='chat_history', tools=self.agent.tools, prompt=self.agent.prompt
        )

    async def send_prompt(self, user_input: str):
        response = self.agent.run(user_input)

        content = response['output'].replace('`', '').replace('json', '', 1)

        # Tentar converter em JSON, algumas respostas não são geradas no formato certo.
        try:
            response = JSONOutput.model_validate_json(content)
        except ValidationError:
            response = {'response': content, 'graph': ''}

        return response

    async def change_model(self, provider: str, model_name: str):
        if provider == 'google':
            self.agent.init_gemini_model(model_name=model_name, temperature=0)
        elif provider == 'groq':
            self.agent.init_groq_model(model_name=model_name, temperature=0)
        else:
            raise ModelNotFoundException('No provider found for the data received.')

        self.agent.initialize_agent(
            memory_key='chat_history', tools=self.agent.tools, prompt=self.agent.prompt
        )

        return
