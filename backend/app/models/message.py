"""
Modelo de dominio para Message.

Por ahora es un dataclass simple.
Al integrar base de datos, este archivo se reemplazara por
un modelo SQLAlchemy (o similar) sin cambiar la logica de negocio.

Campos de IA y reglas:
  - classification: nivel de intencion del lead ("hot" | "warm" | "cold")
  - ai_response: respuesta automatica generada (por AI o por regla)
  - rule_matched: indica si la respuesta fue generada por una regla configurada
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class Message:
    """Representa un mensaje almacenado en el sistema con metadatos de IA y reglas."""

    id: str
    content: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    # Campos enriquecidos por el motor de procesamiento
    classification: Optional[str] = None   # "hot" | "warm" | "cold"
    ai_response: Optional[str] = None      # Respuesta automatica generada
    rule_matched: bool = False             # True si una regla disparo la respuesta