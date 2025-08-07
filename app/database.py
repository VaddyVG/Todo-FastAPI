import logging
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.config import settings


# Логгируем ошибки
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_async_db_url():
    """Получаем правильный асинхронный URL для выбранной БД"""
    db_url = settings.database_url

    # Если используется SQLite, заменяем драйвер на асинхронный
    if db_url.startswith("sqlite://"):
        db_url = db_url.replace("sqlite://", "sqlite+aiosqlite://")
        logger.info("Using async SQLite (aiosqlite driver)")

    return db_url


# Создаем асинхронный движок БД
try:
    db_url = get_async_db_url()
    engine = create_async_engine(
        db_url,
        echo=False,  # Логгировать SQL-запросы
        future=True,  # для совместимости с будущими версиями SQLAlchemy
        connect_args={"check_same_thread": False} if "sqlite" in db_url else {}
    )
    logger.info(f"Database engine created successfully for {db_url}")
except Exception as e:
    logger.error(f"Failed to create database engine: {str(e)}")
    raise


# Настройка асинхронной сессии
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession,
    expire_on_commit=False, autoflush=False
)

Base = declarative_base()

async def get_db():
    """Асинхронный генератор сессий для Dependency Injection"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
