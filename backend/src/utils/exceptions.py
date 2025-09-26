class ModelNotFoundException(Exception):
    """Raised when no llm was instantiated before using agents."""

    def __init__(self, msg: str = None):
        self.msg = (
            msg or 'No llm found, instantiate a model first with the available methods.'
        )


class ExecutorNotFoundException(Exception):
    """Raised when no agent executor was instantiated before using agents."""

    def __init__(self, msg: str = None):
        self.msg = (
            msg
            or 'No agent found, initialize the agent first with initialize_agent method.'
        )


class APIKeyNotFoundException(Exception):
    """Raised when no API key for the desired chat model was found."""

    def __init__(self, msg: str = None):
        self.msg = (
            msg
            or 'Your API key for the desired agent is missing, please export a key as an environment variable.'
        )
