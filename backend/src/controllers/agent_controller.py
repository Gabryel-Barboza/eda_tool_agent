from fastapi import APIRouter, Depends, UploadFile

from src.schemas import ApiKeyInput, UserInput
from src.services import Chat, DataHandler, get_chat_service
from src.settings import settings
from src.utils.exceptions import APIKeyNotFoundException

router = APIRouter(prefix='')
data_handler = DataHandler()


def get_chat_dependency() -> Chat:
    chat_service = get_chat_service()

    if not chat_service:
        raise APIKeyNotFoundException('No API key provided for any service.')

    return chat_service


@router.get('/', status_code=200)
async def ping():
    return True


@router.post('/upload', status_code=201)
async def csv_input(
    separator: str,
    file: UploadFile,
):
    response = await data_handler.load_csv(file, separator)

    return {'data': response}


@router.post('/prompt', status_code=201)
async def prompt_model(input: UserInput, chat: Chat = Depends(get_chat_dependency)):
    response = await chat.send_prompt(input.request)
    return response


@router.put('/change-model', status_code=200)
async def change_model(
    provider: str, model: str, chat: Chat = Depends(get_chat_dependency)
):
    response = await chat.change_model(provider, model)
    return response


@router.post('/send-key', status_code=201)
async def send_key(input: ApiKeyInput):
    if input.provider == 'google':
        settings.gemini_api_key = input.api_key
    elif input.provider == 'groq':
        settings.groq_api_key = input.api_key

    # Força a recriação da instância do chat com a nova chave
    get_chat_service(force_recreate=True)

    return {'detail': 'API Key registered.'}
