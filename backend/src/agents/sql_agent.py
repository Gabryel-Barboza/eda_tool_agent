from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

from .base_agent import BaseAgent


class SQLAgent(BaseAgent):
    def __init__(self):
        prompt_model = ChatPromptTemplate(
            ('system', 'You are a SQL specialist and focused in creating SQL scripts.'),
            ('system', '* use the tool available to execute the scripts you generate'),
            (
                'system',
                '* you are not allowed to create, drop or access other databases',
            ),
            MessagesPlaceholder('agent_scratchpad'),
        )

        # Agent configuration
        self.init_groq_model(temperature=0)
        self.initialize_agent(prompt=prompt_model)
