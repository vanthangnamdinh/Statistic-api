from sqlalchemy import Column, String, DateTime, Integer
from clickhouse_sqlalchemy import make_session, types, engines
from sqlalchemy import create_engine
import uuid

from core.db.clickhouse_session import Base

class StatisticLog(Base):
    __tablename__ = "statistic_log"
    __table_args__ = (engines.Memory(),)

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    local_timestamp = Column(DateTime)
    time_zone = Column(String)
    utc_timestamp = Column(DateTime)
    user_id = Column(String)
    conversation_id = Column(String)
    msg_id = Column(String)
    activity_type = Column(String)
    detail = Column(String)
    current_url = Column(String)
    page_title = Column(String)
    page_description = Column(String)
    page_keywords = Column(types.Array(String))
    user_agent = Column(String)
    extension_version = Column(String)
    agent_name = Column(String)
    agent_version = Column(String)
    string_names = Column(types.Array(String))
    string_values = Column(types.Array(String))
    integer_names = Column(types.Array(String))
    integer_values = Column(types.Array(Integer))
    number_names = Column(types.Array(String))
    number_values = Column(types.Array(types.Float32))
    bool_names = Column(types.Array(String))
    bool_values = Column(
        types.Array(types.UInt8)
    )  # ClickHouse không có Boolean, dùng UInt8
    date_names = Column(types.Array(String))
    date_values = Column(types.Array(DateTime))
