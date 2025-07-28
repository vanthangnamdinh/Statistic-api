from typing import List, Dict, Any, Optional

from pydantic import BaseModel, Field


class StatisticData(BaseModel):
    current_url: Optional[str] = Field(None, description="URL of browser when User sends a message")
    page_title: Optional[str] = Field(None, description="Page title")
    page_description: Optional[str] = Field(None, description="Description of current page")
    page_keywords: Optional[List[str]] = Field(None,
                                               description="An array of strings representing all text on the page")

    def to_dict(self) -> dict:
        return self.dict()


class CreateStatisticLogCommand(BaseModel):
    local_timestamp: Optional[str] = Field(None, description="Time local of log")
    time_zone: Optional[str] = Field(None, description="Timezone of log")
    utc_timestamp: Optional[str] = Field(None, description="UTC Timestamp of log")
    activity_type: Optional[str] = Field(None, description="Activity type")
    detail: Optional[str] = Field(None, description="Detail log")
    user_id: Optional[str] = Field(None, description="Id of User")
    conversation_id: Optional[str] = Field(None, description="Id of conversation")
    msg_id: Optional[str] = Field(None, description="ID of message")
    extension_version: Optional[str] = Field(None, description="Version of chatbot")
    user_agent: Optional[str] = Field(None, description="User context")
    agent_name: Optional[str] = Field(None, description="User context")
    agent_version: Optional[str] = Field(None, description="User context")
    current_url: Optional[str] = Field(None, description="URL of browser when User sends a message")
    page_title: Optional[str] = Field(None, description="Page title")
    page_description: Optional[str] = Field(None, description="Description of current page")
    page_keywords: Optional[List[str]] = Field(None,
                                               description="An array of strings representing all text on the page")
    extra_data: Optional[Dict[str,Any]]= Field(None,
                                               description="Extra data from request")

    def to_dict(self) -> dict:
        # Use `dict` to serialize and ensure nested objects are converted properly
        data = self.dict()
        return data
