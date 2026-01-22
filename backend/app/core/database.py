"""Database connection and session management."""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.core.config import settings
from app.core.logging_config import get_logger


logger = get_logger(__name__)

Base = declarative_base()

# Global engine and session factory (initialized on startup)
engine = None
AsyncSessionLocal = None


async def init_db() -> None:
    """Initialize database connection."""
    global engine, AsyncSessionLocal
    
    if not settings.database_url:
        logger.warning("DATABASE_URL not configured - running without database")
        return
    
    logger.info("Initializing database connection")
    
    engine = create_async_engine(
        settings.database_url,
        echo=settings.db_echo,
        pool_pre_ping=True,  # Verify connections before using
        pool_size=5,
        max_overflow=10,
    )
    
    AsyncSessionLocal = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    # TODO: In production, use Alembic migrations instead
    # For now, create tables if they don't exist
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created/verified")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise


async def close_db() -> None:
    """Close database connection."""
    global engine
    
    if engine:
        logger.info("Closing database connection")
        await engine.dispose()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get database session."""
    if not AsyncSessionLocal:
        raise RuntimeError("Database not initialized")
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def check_db_health() -> bool:
    """Check if database is accessible."""
    if not engine:
        return False
    
    try:
        async with engine.connect() as conn:
            await conn.exec_driver_sql("SELECT 1")
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False
