from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, func
from fastapi import HTTPException
from core.db.clickhouse_session import session
from core.db.clickhouse_models import StatisticLog
import uuid
import json
from datetime import datetime
from typing import Any, List
import logging
from fastapi import Depends


class StatisticLogSQLAlchemyRepo:
    def __init__(self):
        pass

    async def create_log(self, *, data) -> None:
        """Create a new log entry in ClickHouse"""
        types_map = ["string", "integer", "number", "bool", "date"]
        try:
            record_data = {
                "id": str(uuid.uuid4()),
                "local_timestamp": data.local_timestamp if data.local_timestamp else "",
                "time_zone": data.time_zone if data.time_zone else "",
                "utc_timestamp": data.utc_timestamp if data.utc_timestamp else "",
                "user_id": data.user_id if data.user_id else "",
                "conversation_id": data.conversation_id if data.conversation_id else "",
                "msg_id": data.msg_id if data.msg_id else "",
                "activity_type": data.activity_type if data.activity_type else "",
                "detail": data.detail if data.detail else "",
                "_source": json.dumps(data.to_dict()),
                "current_url": data.current_url if data.current_url else "",
                "page_title": data.page_title if data.page_title else "",
                "page_description": (
                    data.page_description if data.page_description else ""
                ),
                "page_keywords": data.page_keywords if data.page_keywords else [],
                "user_agent": data.user_agent if data.user_agent else "",
                "extension_version": (
                    data.extension_version if data.extension_version else ""
                ),
                "agent_name": data.agent_name if data.agent_name else "",
                "agent_version": data.agent_version if data.agent_version else "",
                "string_names": [],
                "string_values": [],
                "integer_names": [],
                "integer_values": [],
                "number_names": [],
                "number_values": [],
                "bool_names": [],
                "bool_values": [],
                "date_names": [],
                "date_values": [],
            }
            logging.info(f"Creating log with data: {record_data}")
            extra_data = getattr(data, "extra_data", {}) or {}
            for key, value in extra_data.items():
                if value is not None:
                    value_type = self._determine_type(value)
                    if value_type in types_map:
                        record_data[f"{value_type}_names"].append(str(key))
                        record_data[f"{value_type}_values"].append(
                            self._convert_value_for_type(value, value_type)
                        )
            session.execute(StatisticLog.__table__.insert(), [record_data])
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500, detail=f"ClickHouse insert error: {str(e)}"
            )
        finally:
            session.close()

    def find_by_user_id(self, user_id: str) -> List[StatisticLog]:
        try:
            result = self.session.execute(
                select(StatisticLog).where(StatisticLog.user_id == user_id)
            )
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Query error: {str(e)}")

    def count_by_user_id(self, user_id: str) -> int:
        try:
            result = self.session.execute(
                select(func.count(StatisticLog.id)).where(
                    StatisticLog.user_id == user_id
                )
            )
            return result.scalar() or 0
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Count error: {str(e)}")

    def _safe_get_string(self, value: Any) -> str:
        return str(value) if value is not None else ""

    def _safe_get_datetime(self, value: Any) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            except Exception:
                return datetime.utcnow()
        return datetime.utcnow()

    def _safe_get_array(self, value: Any) -> List[str]:
        if isinstance(value, list):
            return [str(v) for v in value]
        return []

    def _determine_type(self, value: Any) -> str:
        if isinstance(value, bool):
            return "bool"
        elif isinstance(value, int):
            return "integer"
        elif isinstance(value, float):
            return "number"
        elif isinstance(value, str):
            try:
                datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                return "date"
            except:
                return "string"
        elif isinstance(value, datetime):
            return "date"
        return "string"

    def _convert_value_for_type(self, value: Any, value_type: str) -> Any:
        try:
            if value_type == "integer":
                return int(value)
            elif value_type == "number":
                return float(value)
            elif value_type == "bool":
                return bool(value)
            elif value_type == "date":
                if isinstance(value, str):
                    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                return value
            else:
                return str(value)
        except:
            return str(value)
