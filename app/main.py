import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import router
from app.database import engine, Base


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_tables():
    logger.info("Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Tables created successfully!")


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await create_tables()
        yield
    except Exception as e:
        logger.error(f"Error during startup: {e}", exc_info=True)
        raise
    finally:
        logger.info("Shutting down...")
        await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(router)
