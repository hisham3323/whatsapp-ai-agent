from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class TextContent(BaseModel):
    body: str

class ImageContent(BaseModel):
    mime_type: str
    sha256: str
    id: str

class Message(BaseModel):
    from_number: str = Field(alias="from")
    id: str
    timestamp: str
    type: str
    text: Optional[TextContent] = None
    image: Optional[ImageContent] = None

class Profile(BaseModel):
    name: str

class Contact(BaseModel):
    profile: Profile
    wa_id: str

class Metadata(BaseModel):
    display_phone_number: str
    phone_number_id: str

class Value(BaseModel):
    messaging_product: str
    metadata: Metadata
    contacts: Optional[List[Contact]] = None
    messages: Optional[List[Message]] = None
    # We ignore statuses (like read receipts) for now, but allow the field
    statuses: Optional[List[Dict[str, Any]]] = None

class Change(BaseModel):
    value: Value
    field: str

class Entry(BaseModel):
    id: str
    changes: List[Change]

class WhatsAppWebhookPayload(BaseModel):
    object: str
    entry: List[Entry]