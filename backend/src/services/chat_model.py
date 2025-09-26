from src.agents import AnswerAgent


class Chat:
    def __init__(self):
        self.agent = AnswerAgent()

    def send_prompt(self, question):
        response = self.agent.run(question)

        return response
