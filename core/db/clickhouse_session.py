from clickhouse_sqlalchemy import (
    Table,
    make_session,
    get_declarative_base,
    types,
    engines,
)
from sqlalchemy import create_engine, Column, MetaData

from core.config import config

# ClickHouse async engine với connection string đúng format
clickhouse_engine = create_engine(
    f"clickhouse+native://{config.CLICK_HOUSE_USER}:{config.CLICK_HOUSE_PASSWORD}@{config.CLICK_HOUSE_HOST}:{config.CLICK_HOUSE_PORT}/{config.CLICK_HOUSE_DB}",
)

# ClickHouse session factory
session = make_session(clickhouse_engine)

metadata = MetaData()
metadata.bind = clickhouse_engine

Base = get_declarative_base(metadata=metadata)
