"""
Schemas Pydantic para el recurso Message.

Separan la capa de validacion/serializacion de los modelos de dominio.
Al agregar una DB, estos schemas seguiran igual; solo cambia el modelo.
"""

from pydantic import BaseModel, Field
from datetime import datetime


# --------------------------------------------------------------------------- #
# Schemas de entrada (request)
# --------------------------------------------------------------------------- #


class MessageCreate(BaseModel):
    """Payload esperado al crear un nuevo mensaje."""

    content: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Contenido del mensaje. No puede estar vacio.",
        examples=["Hola, quisiera saber el precio de sus servicios."],
    )


# --------------------------------------------------------------------------- #
# Schemas de salida (response)
# --------------------------------------------------------------------------- #


class MessageResponse(BaseModel):
    """Representacion completa del mensaje con metadatos de IA y reglas."""

    id: str = Field(..., description="Identificador unico del mensaje (UUID).")
    content: str = Field(..., description="Contenido del mensaje.")
    created_at: datetime = Field(..., description="Fecha y hora de creacion (UTC).")

    # -- Campos enriquecidos por el motor de procesamiento -------------------
    classification: str = Field(
        ...,
        description="Nivel de intencion: 'hot' (compra), 'warm' (interes), 'cold' (neutral).",
        examples=["hot", "warm", "cold"],
    )
    response: str = Field(
        ...,
        description="Respuesta automatica generada por regla o IA.",
    )
    rule_matched: bool = Field(
        default=False,
        description="True si la respuesta fue generada por una regla configurada. False si fue el AI.",
    )

    model_config = {"from_attributes": True}