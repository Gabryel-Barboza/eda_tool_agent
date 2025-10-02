from fastapi import APIRouter, UploadFile

from src.schemas import UserInput
from src.services import DataHandler, get_chat_service

router = APIRouter()
data_handler = DataHandler()
chat = get_chat_service()


@router.post('/upload', status_code=201)
async def csv_input(file: UploadFile):
    await data_handler.load_csv(file)

    return {'detail': 'File uploaded successfully'}


@router.post('/prompt', status_code=201)
async def prompt_model(input: UserInput):
    response = await chat.send_prompt(input.request)

    return response


@router.put('/change-model', status_code=200)
async def change_model(provider: str, model: str):
    response = await chat.change_model(provider, model)

    return response
