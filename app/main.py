from fastapi import FastAPI

from app.startup import configure_app
from app.constants import API_TITLE
from app.api.upload import router as upload_router
from app.api.query import router as query_router
from app.api.report import router as report_router

app = FastAPI(title=API_TITLE)

configure_app(app)
app.include_router(upload_router)
app.include_router(query_router)
app.include_router(report_router)


@app.get('/')
async def health_check():
    return {'message': 'Welcome to RAG Document QA API'}
