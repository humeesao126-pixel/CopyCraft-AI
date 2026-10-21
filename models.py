
from pydantic import BaseModel, Field


class MarketingCopyRequest(BaseModel):
    """Validate user-provided marketing details."""

    product_name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    platform: str
    tone: str

    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)


class MarketingCopyResponse(BaseModel):
    """Validate structured marketing content."""

    product_name: str
    platform: str
    tone: str
    headline: str
    body: str
    call_to_action: str
