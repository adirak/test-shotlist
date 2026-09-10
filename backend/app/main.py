from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.config import get_settings
from app.db import engine
from app.routers import shots

app = FastAPI(title="ShotList API")
settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(shots.router)


@app.get("/health")
async def health():
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    return {"status": "ok", "env": settings.env}
