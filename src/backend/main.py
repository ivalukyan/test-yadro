from fastapi import FastAPI

from database.engine import create_tables, drop_tables

from backend.routers.router_grafs import router as graph_router


app = FastAPI(
    title='Test Yadro',
)

@app.on_event("startup")
async def create_models_database():
    await drop_tables()
    await create_tables()


@app.get("/health")
async def health_check():
    return {"status": "ok"}


app.include_router(graph_router)
