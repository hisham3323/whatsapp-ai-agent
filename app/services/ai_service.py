import logging
import httpx
from app.core.config import settings
from app.services.db_service import save_message, get_conversation_history

logger = logging.getLogger(__name__)

async def generate_ai_response(
    user_message: str, 
    system_prompt: str, 
    user_phone: str, 
    model: str = "openrouter/free" 
) -> str:
    """
    Calls OpenRouter and uses the PostgreSQL database for permanent memory.
    """
    if not settings.OPENROUTER_API_KEY:
        logger.warning("OPENROUTER_API_KEY is missing.")
        return "I am currently under maintenance. Please check back later!"

    # 1. Save the user's incoming message to the database immediately
    await save_message(user_phone, "user", user_message)

    # 2. Fetch the user's permanent history from the database
    history = await get_conversation_history(user_phone)

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost:8000", 
        "X-Title": settings.PROJECT_NAME,
        "Content-Type": "application/json"
    }
    
    # 3. Combine the System Prompt with the database history
    messages_payload = [{"role": "system", "content": system_prompt}] + history
    
    payload = {
        "model": model,
        "messages": messages_payload 
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=payload, timeout=30.0)
            response.raise_for_status() 
            data = response.json()
            
            ai_reply = data["choices"][0]["message"]["content"].strip()
            
            # 4. Save the AI's reply to the database so it remembers what it said
            await save_message(user_phone, "assistant", ai_reply)
            
            return ai_reply
            
        except Exception as e:
            logger.error(f"Error in AI service: {e}")
            return "Something went wrong on my end! Please hold on."