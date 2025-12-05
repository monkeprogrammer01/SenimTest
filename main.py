from typing import Union
from auth.routes.auth_router import router
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(router)