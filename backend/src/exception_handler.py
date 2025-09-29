from zipfile import BadZipFile

from fastapi import status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src.utils.exceptions import (
    APIKeyNotFoundException,
    ModelNotFoundException,
    WrongFileTypeError,
)


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)

            return response
        except (
            APIKeyNotFoundException,
            WrongFileTypeError,
            ModelNotFoundException,
        ) as exc:
            return JSONResponse(
                content=exc.msg, status_code=status.HTTP_400_BAD_REQUEST
            )
        except BadZipFile:
            return JSONResponse(
                content='Bad zip file sent, maybe the file is corrupted or empty.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        except FileNotFoundError as exc:
            return JSONResponse(
                content=exc.strerror,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
