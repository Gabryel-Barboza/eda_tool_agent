from src.agents import AnswerAgent
from src.schemas import JSONOutput
from src.utils.exceptions import ModelNotFoundException


class Chat:
    def __init__(self):
        self.agent = AnswerAgent()

    async def send_prompt(self, input: str):
        output_instructions = self.agent.get_json_parser(JSONOutput)
        response = self.agent.run(input, output_instructions)
        response = JSONOutput.model_validate_json(response['output'])

        return response

    async def change_model(self, provider: str, model_name: str):
        if provider == 'google':
            self.agent.init_gemini_model(model_name=model_name, temperature=0)
        elif provider == 'groq':
            self.agent.init_groq_model(model_name=model_name, temperature=0)
        else:
            raise ModelNotFoundException('No provider found for the data received.')

        self.agent.initialize_agent(tools=self.agent.tools, prompt=self.agent.prompt)

        return
