# main.py

from fastapi import FastAPI
from .api import upload, status

app = FastAPI()

app.include_router(upload.router, tags=["upload"], prefix="/api")
app.include_router(status.router, tags=["status"], prefix="/api")
