from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from app.api.v1.chat.router import api as chat

v1 = APIRouter()

v1.include_router(chat, prefix='/chat', default_response_class=ORJSONResponse)
