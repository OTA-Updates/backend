from pydantic import BaseModel, Field


class BaseErrorSchema(BaseModel):
    status_code: str = Field(alias="statusCode")
    message: str
