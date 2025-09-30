from fastapi import FastAPI
from app.v1 import chat,prefill

app = FastAPI()

#routes
app.include_router(chat.router,prefix="/v1/chat")
app.include_router(prefill.router,prefix="/v1")