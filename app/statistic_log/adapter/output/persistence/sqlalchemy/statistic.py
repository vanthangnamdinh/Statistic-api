import json

import uuid
from datetime import datetime

from app.statistic_log.domain.repository.statistic import StatisticRepo
from core.db.clickhouse_db import clickhouse_manager

def is_valid_datetime_format(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False

def determine_type(value):
    if isinstance(value, str):
        if is_valid_datetime_format(value):
            return "date"
        return "string"
    elif isinstance(value, int):
        return 'integer'
    elif isinstance(value, float):
        return 'number'
    elif isinstance(value, bool):
        return 'bool'
    return 'string'


class StatisticLogRepo(StatisticRepo):
    async def create_log(self, *, data) -> None:

        types_map=["string","interger","number","bool","date"]
       
        try:
            # clickhouse_manager = ClickHouse()
            # Insert the data into ClickHouse

            record = {
                "id": str(uuid.uuid4()),
                "local_timestamp": data.local_timestamp if data.local_timestamp else "",
                "time_zone": data.time_zone if data.time_zone else "",
                "utc_timestamp": data.utc_timestamp if data.utc_timestamp else "",
                "user_id": data.user_id if data.user_id else "",
                "conversation_id": data.conversation_id if data.conversation_id else "",
                "msg_id": data.msg_id if data.msg_id else "",
                "activity_type": data.activity_type if data.activity_type else "",
                "detail": data.detail if data.detail else "",
                "_source": json.dumps(data.to_dict()) ,
                "current_url": data.current_url if data.current_url else "",
                "page_title": data.page_title if data.page_title else "",
                "page_description": data.page_description if data.page_description else "",
                "page_keywords": data.page_keywords if data.page_keywords else [],
                "user_agent": data.user_agent if data.user_agent else "",
                "extension_version": data.extension_version if data.extension_version else "",
                "agent_name": data.agent_name if data.agent_name else "",
                "agent_version": data.agent_version if data.agent_version else "",
                "string_names":[],
                "string_values":[],
                "integer_names":[],
                "integer_values":[],
                "number_names":[],
                "number_values":[],
                "bool_names":[],
                "bool_values":[],
                "date_names":[],
                "date_values":[]
            }
            extra_data=data.extra_data if data.extra_data else {}
            for key, value in extra_data.items():
                value_type = determine_type(value)
                if value_type in types_map:
                   record[f'{value_type}_names'].append(key)
                   record[f'{value_type}_values'].append(value)
            
            await clickhouse_manager.insert_one("statistic_log", record)
            # await clickhouse_manager.create_db("statistic")
            # await clickhouse_manager.create_table("statistic_log")
            # await  clickhouse_manager.drop_table("statistic_log")

        except Exception as e:
            raise Exception(str(e))
