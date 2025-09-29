from fastapi import APIRouter, UploadFile

from src.schemas import UserInput
from src.services import Chat, DataInserter

router = APIRouter()
data_inserter = DataInserter()
chat = Chat()


@router.post('/upload', status_code=201)
async def csv_input(file: UploadFile):
    isZip = file.content_type == 'application/zip'
    response = await data_inserter.process_csv(file, isZip)

    return response


@router.post('/prompt', status_code=201)
async def prompt_model(input: UserInput):
    response = await chat.send_prompt(input.request)

    return response


@router.put('/change-model', status_code=200)
async def change_model(provider: str, model: str):
    response = await chat.change_model(provider, model)

    return response
