from fastapi import APIRouter, UploadFile

from src.schemas import ApiKeyInput, UserInput
from src.services import DataHandler, get_chat_service
from src.settings import settings
from src.utils.exceptions import APIKeyNotFoundException

router = APIRouter()
data_handler = DataHandler()
chat = get_chat_service()


@router.post('/upload', status_code=201)
async def csv_input(file: UploadFile):
    await data_handler.load_csv(file)

    return {'detail': 'File uploaded successfully'}


@router.post('/prompt', status_code=201)
async def prompt_model(input: UserInput):
    if chat:
        response = await chat.send_prompt(input.request)
    else:
        raise APIKeyNotFoundException

    return response


@router.put('/change-model', status_code=200)
async def change_model(provider: str, model: str):
    if chat:
        response = await chat.change_model(provider, model)
    else:
        raise APIKeyNotFoundException

    return response


@router.post('/send-key', status_code=201)
async def send_key(input: ApiKeyInput):
    global chat

    if input.provider == 'google':
        settings.gemini_api_key = input.api_key
    elif input.provider == 'groq':
        settings.groq_api_key = input.api_key

    chat = get_chat_service()

    return {}
