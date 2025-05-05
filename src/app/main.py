from fastapi import FastAPI

from src.database.engine import create_tables, drop_tables

from src.app.routers.router_grafs import router as graph_router


app = FastAPI(
    title='Test Yadro',
)

@app.lifespan("startup")
async def create_models_database():
    await drop_tables()
    await create_tables()


app.include_router(graph_router)
