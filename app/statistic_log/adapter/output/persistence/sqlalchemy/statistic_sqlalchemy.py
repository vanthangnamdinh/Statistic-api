import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from app.statistic_log.domain.repository.statistic import StatisticRepo
from core.db.clickhouse_models import StatisticLog
from core.db.clickhouse_session import ClickHouseSession


def is_valid_datetime_format(date_string: str) -> bool:
    """Check if string is in valid datetime format"""
    try:
        datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False


def determine_type(value: Any) -> str:
    """Determine the type of a value for ClickHouse storage"""
    if isinstance(value, bool):  # Check bool first since bool is subclass of int
        return 'bool'
    elif isinstance(value, int):
        return 'integer'
    elif isinstance(value, float):
        return 'number'
    elif isinstance(value, str):
        if is_valid_datetime_format(value):
            return "date"
        return "string"
    elif isinstance(value, datetime):
        return "date"
    else:
        return 'string'  # Default fallback


class StatisticLogSQLAlchemyRepo(StatisticRepo):
    def __init__(self):
        """Initialize repository without session - session will be managed per operation"""
        pass

    async def create_log(self, *, data) -> None:
        """Create a new log entry in ClickHouse"""
        types_map = ["string", "integer", "number", "bool", "date"]
        
        async with ClickHouseSession() as session:
            try:
                # Prepare base record data
                record_data = {
                    "id": str(uuid.uuid4()),
                    "local_timestamp": self._safe_get_datetime(data.local_timestamp),
                    "time_zone": self._safe_get_string(data.time_zone),
                    "utc_timestamp": self._safe_get_datetime(data.utc_timestamp),
                    "user_id": self._safe_get_string(data.user_id),
                    "conversation_id": self._safe_get_string(data.conversation_id),
                    "msg_id": self._safe_get_string(data.msg_id),
                    "activity_type": self._safe_get_string(data.activity_type),
                    "detail": self._safe_get_string(data.detail),
                    "_source": json.dumps(data.to_dict()) if hasattr(data, 'to_dict') else json.dumps({}),
                    "current_url": self._safe_get_string(data.current_url),
                    "page_title": self._safe_get_string(data.page_title),
                    "page_description": self._safe_get_string(data.page_description),
                    "page_keywords": self._safe_get_array(data.page_keywords),
                    "user_agent": self._safe_get_string(data.user_agent),
                    "extension_version": self._safe_get_string(data.extension_version),
                    "agent_name": self._safe_get_string(data.agent_name),
                    "agent_version": self._safe_get_string(data.agent_version),
                    "string_names": [],
                    "string_values": [],
                    "integer_names": [],
                    "integer_values": [],
                    "number_names": [],
                    "number_values": [],
                    "bool_names": [],
                    "bool_values": [],
                    "date_names": [],
                    "date_values": []
                }

                # Process extra_data with proper type handling
                extra_data = getattr(data, 'extra_data', {}) or {}
                for key, value in extra_data.items():
                    if value is not None:  # Skip None values
                        value_type = determine_type(value)
                        if value_type in types_map:
                            record_data[f'{value_type}_names'].append(str(key))
                            record_data[f'{value_type}_values'].append(self._convert_value_for_type(value, value_type))

                # Create and insert using SQLAlchemy
                log_record = StatisticLog(**record_data)
                session.add(log_record)
                await session.commit()

            except SQLAlchemyError as e:
                await session.rollback()
                raise HTTPException(status_code=500, detail=f"Database error while creating log: {str(e)}")
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=500, detail=f"Unexpected error while creating log: {str(e)}")

    def _safe_get_string(self, value: Any) -> str:
        """Safely get string value with fallback"""
        return str(value) if value is not None else ""

    def _safe_get_datetime(self, value: Any) -> Optional[datetime]:
        """Safely get datetime value"""
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, str) and is_valid_datetime_format(value):
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return None

    def _safe_get_array(self, value: Any) -> List[str]:
        """Safely get array value"""
        if value is None:
            return []
        if isinstance(value, list):
            return [str(item) for item in value]
        return []

    def _convert_value_for_type(self, value: Any, value_type: str) -> Any:
        """Convert value to appropriate type for ClickHouse"""
        try:
            if value_type == "integer":
                return int(value)
            elif value_type == "number":
                return float(value)
            elif value_type == "bool":
                return bool(value)
            elif value_type == "date":
                if isinstance(value, str):
                    return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                return value
            else:  # string
                return str(value)
        except (ValueError, TypeError):
            # If conversion fails, return as string
            return str(value)

    async def find_by_user_id(self, user_id: str) -> List[StatisticLog]:
        """Find all logs by user_id"""
        async with ClickHouseSession() as session:
            try:
                result = await session.execute(
                    select(StatisticLog).where(StatisticLog.user_id == user_id)
                )
                return list(result.scalars().all())
            except SQLAlchemyError as e:
                raise Exception(f"Database error while finding by user_id: {str(e)}")

    async def find_by_activity_type(self, activity_type: str) -> List[StatisticLog]:
        """Find all logs by activity_type"""
        async with ClickHouseSession() as session:
            try:
                result = await session.execute(
                    select(StatisticLog).where(StatisticLog.activity_type == activity_type)
                )
                return list(result.scalars().all())
            except SQLAlchemyError as e:
                raise Exception(f"Database error while finding by activity_type: {str(e)}")

    async def find_by_date_range(self, start_date: datetime, end_date: datetime) -> List[StatisticLog]:
        """Find logs within date range"""
        async with ClickHouseSession() as session:
            try:
                result = await session.execute(
                    select(StatisticLog).where(
                        StatisticLog.utc_timestamp >= start_date,
                        StatisticLog.utc_timestamp <= end_date
                    )
                )
                return list(result.scalars().all())
            except SQLAlchemyError as e:
                raise Exception(f"Database error while finding by date range: {str(e)}")

    async def count_by_user_id(self, user_id: str) -> int:
        """Count logs by user_id"""
        async with ClickHouseSession() as session:
            try:
                from sqlalchemy import func
                result = await session.execute(
                    select(func.count(StatisticLog.id)).where(StatisticLog.user_id == user_id)
                )
                return result.scalar() or 0
            except SQLAlchemyError as e:
                raise Exception(f"Database error while counting by user_id: {str(e)}")
