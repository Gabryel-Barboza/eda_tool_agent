from fastapi import APIRouter, UploadFile

from src.schemas import JSONOutput, UserInput
from src.services import Chat, DataInserter

router = APIRouter()
data_inserter = DataInserter()
chat = Chat()


@router.post('/upload', status_code=201)
async def csv_input(data: UploadFile):
    isZip = data.content_type == 'application/zip'
    response = await data_inserter.process_csv(data, isZip)

    return response


@router.post('/prompt', status_code=201)
async def prompt_model(input: UserInput) -> JSONOutput:
    response = await chat.send_prompt(input)

    return response


@router.put('/change-model', status_code=200)
async def change_model(provider: str, model: str):
    await chat.change_model(provider, model)

    return {}
