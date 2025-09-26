from fastapi import FastAPI

from .controllers import agent_controller

app = FastAPI(
    title='API SophIA EDA',
    summary='API para controle de requisições para os agentes de análise de dados.',
    root_path='/api',
    version='0.1.0',
)

app.include_router(agent_controller.router)
