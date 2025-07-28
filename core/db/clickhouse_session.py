from clickhouse_sqlalchemy import make_session, get_declarative_base, types, engines
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from core.config import config

# ClickHouse async engine với connection string đúng format
clickhouse_engine = create_engine(
    f"clickhouse+asynch://{config.CLICK_HOUSE_USER}:{config.CLICK_HOUSE_PASSWORD}@{config.CLICK_HOUSE_HOST}:{config.CLICK_HOUSE_PORT}/{config.CLICK_HOUSE_DB}",
    echo=config.DEBUG,
    future=True,
    # Thêm các option cho ClickHouse
    pool_pre_ping=True,
    pool_recycle=3600,
)

# ClickHouse session factory
ClickHouseSession = async_sessionmaker(
    bind=clickhouse_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,  # Tắt autoflush cho ClickHouse
    autocommit=False
)

async def get_clickhouse_session() -> AsyncSession:
    """Dependency for getting ClickHouse session"""
    async with ClickHouseSession() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
