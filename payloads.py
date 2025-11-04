from pydantic import BaseModel


# User input payload (content only)
class ContentOnlyMessagePayload(BaseModel):
    message: str
