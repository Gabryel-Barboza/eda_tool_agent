from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .controllers import agent_controller
from .utils.exceptions import APIKeyNotFoundException, ModelNotFoundException

app = FastAPI(
    title='API SophIA EDA',
    summary='API para controle de requisições para os agentes de análise de dados.',
    root_path='/api',
    version='0.1.0',
)

app.include_router(agent_controller.router)


@app.exception_handler(APIKeyNotFoundException)
async def handleAPIKeyNotFoundException(request: Request, exc: APIKeyNotFoundException):
    return JSONResponse(content=exc.msg, status_code=400)


@app.exception_handler(ModelNotFoundException)
async def handleModelNotFoundException(request: Request, exc: ModelNotFoundException):
    return JSONResponse(content=exc.msg, status_code=400)
