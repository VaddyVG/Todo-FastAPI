import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import router
from app.database import engine, Base


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Creating database tables...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Tables created successfully!")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        raise

    yield

    logger.info("Shutting down...")
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(router)
