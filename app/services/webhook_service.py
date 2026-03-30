import logging
from app.core.redis import get_redis

logger = logging.getLogger(__name__)

async def is_message_processed(message_id: str) -> bool:
    """
    Checks Redis to see if we have already processed this WhatsApp message ID.
    If not, it marks it as processed with a 24-hour expiration.
    Returns True if already processed (duplicate), False if it's a new message.
    """
    redis_key = f"wa_msg:{message_id}"
    
    redis_client = await get_redis()
    
    # We use Redis SET with NX (Set if Not eXists) to prevent race conditions.
    # ex=86400 sets an expiration of 24 hours so our Redis memory doesn't fill up forever.
    # If set returns True, the key was successfully created (new message).
    # If set returns False/None, the key already existed (duplicate message).
    is_new = await redis_client.set(redis_key, "1", ex=86400, nx=True)
    
    if not is_new:
        logger.info(f"Duplicate message detected. ID {message_id} already processed. Skipping.")
        return True
        
    return False