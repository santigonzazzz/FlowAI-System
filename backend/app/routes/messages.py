"""
Router de mensajes — expone los endpoints:
  POST /messages  → crear mensaje
  GET  /messages  → listar mensajes

Cada ruta delega el trabajo al servicio correspondiente.
Las rutas no contienen lógica de negocio.
"""

from typing import List

from fastapi import APIRouter, status

from app.schemas.message import MessageCreate, MessageResponse
from app.services.message_service import create_message, get_all_messages

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un mensaje",
    description="Recibe un JSON con `content` y persiste el mensaje. Retorna el mensaje con su id y timestamp.",
)
def post_message(payload: MessageCreate) -> MessageResponse:
    """
    Crea un nuevo mensaje.

    - **content**: texto del mensaje (1–2000 caracteres, requerido).
    """
    return create_message(payload)


@router.get(
    "",
    response_model=List[MessageResponse],
    summary="Listar todos los mensajes",
    description="Retorna la lista completa de mensajes almacenados. Vacía si no hay ninguno.",
)
def list_messages() -> List[MessageResponse]:
    """Retorna todos los mensajes en memoria."""
    return get_all_messages()
