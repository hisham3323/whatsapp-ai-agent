import logging
from fastapi import APIRouter, Request, Query, HTTPException, status, BackgroundTasks
from fastapi.responses import PlainTextResponse
 
from app.core.config import settings
from app.schemas.whatsapp import WhatsAppWebhookPayload
from app.services.webhook_service import is_message_processed
from app.services.ai_service import generate_ai_response
from app.services.whatsapp_service import send_whatsapp_message
from app.services.db_service import get_inventory_list
 
logger = logging.getLogger(__name__)
router = APIRouter()
 
@router.get("/webhook")
async def verify_webhook(
    mode: str = Query(None, alias="hub.mode"),
    token: str = Query(None, alias="hub.verify_token"),
    challenge: str = Query(None, alias="hub.challenge")
):
    if mode and token:
        if mode == "subscribe" and token == settings.WHATSAPP_VERIFY_TOKEN:
            logger.info("Webhook verified successfully.")
            return PlainTextResponse(content=challenge, status_code=status.HTTP_200_OK)
        else:
            logger.warning("Webhook verification failed: Token mismatch.")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Verification token mismatch"
            )
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Missing parameters"
    )
 
async def process_and_reply(sender_phone: str, user_text: str):
    """
    Background task to handle the heavy lifting: talking to AI and sending the reply.
    """
    # 1. Fetch the live inventory from the PostgreSQL database
    inventory_context = await get_inventory_list()
    
    # 2. Give the AI its personality AND the live store data
    system_prompt = (
        "You are a friendly and helpful AI shopping assistant for our store. "
        "Keep your answers concise, conversational, and helpful. "
        "When a user asks about products, only recommend items from the inventory below. "
        f"\n\n{inventory_context}"
    )
    
    # 3. Generate the AI response
    logger.info(f"Generating AI response for {sender_phone}...")
    ai_reply = await generate_ai_response(user_text, system_prompt, sender_phone)
    
    # 4. Send the reply back to the user
    logger.info(f"Sending reply to {sender_phone}...")
    await send_whatsapp_message(sender_phone, ai_reply)
 
@router.post("/webhook")
async def receive_message(payload: WhatsAppWebhookPayload, background_tasks: BackgroundTasks):
    try:
        for entry in payload.entry:
            for change in entry.changes:
                value = change.value
                
                if value.messages:
                    for message in value.messages:
                        msg_id = message.id
                        
                        # 1. Idempotency Check
                        if await is_message_processed(msg_id):
                            continue 
                            
                        sender_phone = message.from_number
                        
                        # We only process text messages for now
                        if message.type == "text" and message.text:
                            user_text = message.text.body
                            logger.info(f"New text message from {sender_phone}: {user_text}")
                            
                            # 2. Hand off to background task
                            # This allows us to return the 200 OK to Meta instantly
                            background_tasks.add_task(process_and_reply, sender_phone, user_text)
                        else:
                            logger.info(f"Received non-text message type: {message.type}. Ignoring for now.")
 
        # Instantly return success to Meta
        return {"status": "success"}
    
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return {"status": "error"}