from fastapi import APIRouter, Body, UploadFile
from typing_extensions import Annotated

from src.services import Chat, DataInserter

router = APIRouter()


@router.post('/upload')
async def csv_input(data: UploadFile):
    data_inserter = DataInserter()
    response = data_inserter.process_csv(data)

    return response


@router.post('/prompt')
async def prompt_model(question: Annotated[str, Body()]):
    chat = Chat()
    response = chat.send_prompt(question)

    return response
