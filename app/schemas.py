from pydantic import BaseModel, Field

class MemoryCreate(BaseModel):
    contact_key: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1, max_length=5000)
    source: str = Field(default="manual", max_length=80)

class DraftRequest(BaseModel):
    message_id: str
    tone: str = "professional"
    extra_context: str = ""

class DraftResponse(BaseModel):
    message_id: str
    contact_key: str
    context_used: list[str]
    draft: str
