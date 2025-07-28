import uuid
from datetime import datetime
from typing import Any, List

from sqlalchemy import String, Text, types, JSON, ARRAY, Integer, Float, Boolean, Date
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base
from core.db.mixins import TimestampMixin


class StatisticLog(Base, TimestampMixin):
    __tablename__ = "statistic_log"

    id: Mapped[uuid.UUID] = mapped_column(types.Uuid, primary_key=True, )
    local_timestamp: Mapped[datetime] = mapped_column(nullable=True)
    time_zone: Mapped[datetime] = mapped_column(nullable=True)
    utc_timestamp: Mapped[datetime] = mapped_column(nullable=True)
    user_id: Mapped[str] = mapped_column(String(255), nullable=True)
    conversation_id: Mapped[str] = mapped_column(String(255), nullable=True)
    msg_id: Mapped[str] = mapped_column(String(255), nullable=True)
    activity_type: Mapped[datetime] = mapped_column(String(255), nullable=True)
    detail: Mapped[dict[str, Any]:JSON] = mapped_column(type_=JSON, nullable=True)
    _source: Mapped[str] = mapped_column(Text, nullable=True)
    current_url: Mapped[str] = mapped_column(String(255), nullable=True)
    page_title: Mapped[str] = mapped_column(String(255), nullable=True)
    page_description: Mapped[str] = mapped_column(Text, nullable=True)
    page_keywords: Mapped[List[str]] = mapped_column(type_=ARRAY(String), nullable=True)
    user_agent: Mapped[str] = mapped_column(String(255), nullable=True)
    extension_version: Mapped[str] = mapped_column(String(255), nullable=True)
    agent_name: Mapped[str] = mapped_column(String(255), nullable=True)
    agent_version: Mapped[str] = mapped_column(String(255), nullable=True)
    string_names: Mapped[List[str]] = mapped_column(type_=ARRAY(String), nullable=True)
    string_values: Mapped[List[str]] = mapped_column(type_=ARRAY(String), nullable=True)
    integer_names: Mapped[List[str]] = mapped_column(type_=ARRAY(String), nullable=True)
    integer_values: Mapped[List[int]] = mapped_column(type_=ARRAY(Integer), nullable=True)
    number_names: Mapped[List[str]] = mapped_column(type_=ARRAY(String), nullable=True)
    number_values: Mapped[List[float]] = mapped_column(type_=ARRAY(Float), nullable=True)
    bool_names: Mapped[List[str]] = mapped_column(type_=ARRAY(String), nullable=True)
    bool_values: Mapped[List[bool]] = mapped_column(type_=ARRAY(Boolean), nullable=True)
    date_names: Mapped[List[str]] = mapped_column(type_=ARRAY(String), nullable=True)
    date_values: Mapped[List[datetime]] = mapped_column(type_=ARRAY(Date), nullable=True)
