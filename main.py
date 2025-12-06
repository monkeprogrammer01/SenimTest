from typing import Union
from auth.routes.auth_router import router
from fastapi import FastAPI
from report.routes.report_router import report_router
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(router)
app.include_router(report_router)