from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .controllers import agent_controller, db_controller
from .exception_handler import ExceptionHandlerMiddleware

app = FastAPI(
    title='API SophIA EDA',
    summary='API para controle de requisições para os agentes de análise de dados.',
    root_path='/api',
    version='0.1.0',
)

origins = [
    '*',
]

# CORS para restrição de domínios, liberal por padrão.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.add_middleware(ExceptionHandlerMiddleware)

app.include_router(agent_controller.router)
app.include_router(db_controller.router)
