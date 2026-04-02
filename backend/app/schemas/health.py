"""
Schemas Pydantic para respuestas generales del sistema.
"""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Respuesta del endpoint de salud."""

    status: str
