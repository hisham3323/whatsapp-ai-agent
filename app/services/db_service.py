from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.product import Product
from app.models.message import Message

async def get_inventory_list() -> str:
    """Fetches all products from the database and formats them for the AI."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Product))
        products = result.scalars().all()
        
        if not products:
            return "Our inventory is currently empty."
            
        inventory_text = "CURRENT STORE INVENTORY:\n"
        for p in products:
            inventory_text += f"- {p.name}: ${p.price:.2f} ({p.description})\n"
            
        return inventory_text

async def save_message(phone_number: str, role: str, content: str):
    """Saves a single message to the database."""
    async with AsyncSessionLocal() as session:
        new_msg = Message(phone_number=phone_number, role=role, content=content)
        session.add(new_msg)
        await session.commit()

async def get_conversation_history(phone_number: str, limit: int = 10) -> list:
    """Fetches the last N messages for a user and formats them for OpenRouter."""
    async with AsyncSessionLocal() as session:
        # Get the latest messages for this phone number, sorted by newest first
        stmt = select(Message).where(Message.phone_number == phone_number).order_by(Message.timestamp.desc()).limit(limit)
        result = await session.execute(stmt)
        messages = result.scalars().all()
        
        # Reverse them so they are in chronological order for the AI to read naturally
        history = []
        for msg in reversed(messages):
            history.append({"role": msg.role, "content": msg.content})
            
        return history