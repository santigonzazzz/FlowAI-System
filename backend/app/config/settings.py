"""
Configuración central de la aplicación.
Usa Pydantic Settings para gestionar variables de entorno.
Preparado para escalar: agregar DB_URL, SECRET_KEY, etc.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    # Metadatos de la app
    APP_NAME: str = "FlowAI API"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "API backend escalable construida con FastAPI"
    DEBUG: bool = False

    # -- Groq / IA ------------------------------------------------------------
    GROQ_API_KEY: Optional[str] = None
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"
    # Modelo principal. Alternativas rapidas: "llama-3.1-8b-instant"
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # Preparado para base de datos (sin usar aun)
    # DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost/db"

    model_config = {
        "env_file": ".env",
        # utf-8-sig elimina el BOM automaticamente si el archivo lo tiene
        "env_file_encoding": "utf-8-sig",
        "extra": "ignore",   # ignora claves desconocidas del .env
    }


@lru_cache()
def get_settings() -> Settings:
    """
    Retorna una instancia cacheada de Settings.
    Usar lru_cache evita releer el .env en cada request.
    """
    return Settings()