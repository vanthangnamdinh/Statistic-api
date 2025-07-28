from clickhouse_sqlalchemy import make_session
from sqlalchemy import create_engine
from core.config import config

# ClickHouse async engine với connection string đúng format
clickhouse_engine = create_engine(
    f"clickhouse+asynch://{config.CLICK_HOUSE_USER}:{config.CLICK_HOUSE_PASSWORD}@{config.CLICK_HOUSE_HOST}:{config.CLICK_HOUSE_PORT}/{config.CLICK_HOUSE_DB}",
    echo=config.DEBUG,
    future=True,
    # Thêm các option cho ClickHouse
    pool_pre_ping=True,
    # pool_recycle=3600,  # Không cần thiết cho ClickHouse
    # pool_size=10,  # Không cần thiết cho ClickHouse
    # Tắt các tính năng không cần thiết
    pool_use_lifo=False,
)

# ClickHouse session factory
ClickHouseSession = make_session(
   clickhouse_engine
)

async def get_clickhouse_session() :
    """Dependency for getting ClickHouse session"""
    async with ClickHouseSession() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
