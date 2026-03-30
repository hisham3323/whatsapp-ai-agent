import logging
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)

async def send_whatsapp_message(to_number: str, text_body: str) -> bool:
    """
    Sends a text message back to the user via the WhatsApp Cloud API.
    """
    if not settings.WHATSAPP_TOKEN or not settings.WHATSAPP_PHONE_NUMBER_ID:
        logger.error("Missing WhatsApp credentials in environment variables.")
        return False

    # Meta Graph API endpoint for sending messages (using v19.0)
    url = f"https://graph.facebook.com/v19.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # This is the exact JSON structure Meta requires to send a text message
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {
            "body": text_body
        }
    }
    
    async with httpx.AsyncClient() as client:
        try:
            # We send the POST request to Meta
            response = await client.post(url, headers=headers, json=payload, timeout=10.0)
            response.raise_for_status() # This will throw an error if Meta rejects our message
            
            logger.info(f"Successfully sent WhatsApp message to {to_number}")
            return True
            
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to send message. Meta returned HTTP {e.response.status_code}: {e.response.text}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending WhatsApp message: {e}")
            return False