from fastapi import FastAPI, Request
import time
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from .notes import notes

from .db import init_db, get_session

class LiveMessage(BaseModel):
    name : str
    message : str = Field(default=None, title="Message", max_length=300)

origins = [
    "http://localhost",
    "http://localhost:3000"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(notes.router)

@app.on_event("startup")
def on_startup():
    init_db()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/")
def main():
    return LiveMessage(name="Server", message="Live")

