from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str = "WhatsApp AI Sales Agent"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # OpenRouter API
    OPENROUTER_API_KEY: str = ""

    # WhatsApp Cloud API
    WHATSAPP_VERIFY_TOKEN: str = ""
    WHATSAPP_TOKEN: str = ""  # <--- We ensure it is exactly this!
    WHATSAPP_PHONE_NUMBER_ID: str = ""
    WHATSAPP_API_VERSION: str = "v18.0"

    # PostgreSQL Database
    DATABASE_URL: str = ""

    # Redis
    REDIS_URL: str = ""

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

settings = Settings()