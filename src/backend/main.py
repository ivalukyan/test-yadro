import logging

from fastapi import FastAPI

from src.database.engine import create_tables, drop_tables
from src.backend.routers.router_grafs import router as graph_router

logger = logging.getLogger(__name__)


app = FastAPI(
    title='Test Yadro',
)

@app.on_event("startup")
async def create_models_database():
    await drop_tables()
    await create_tables()
    logger.info("Database created")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


app.include_router(graph_router)
