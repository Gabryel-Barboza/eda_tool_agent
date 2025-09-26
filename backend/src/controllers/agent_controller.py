from fastapi import APIRouter

router = APIRouter()


@router.get('/')
async def test():
    return 'Hello, World!'


@router.post('/upload')
async def csv_input():
    pass


@router.post('/prompt')
async def prompt_model():
    pass
