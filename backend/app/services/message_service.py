"""
Servicio de mensajes — capa de logica de negocio.

Responsabilidades:
  - Crear mensajes con ID unico
  - Procesar mensajes usando el motor de reglas PRIMERO, luego IA
  - Recuperar todos los mensajes

Flujo de procesamiento:
    1. rule_engine.apply_rules()  → busca coincidencia en reglas configuradas
    2a. Si HAY match             → usa los overrides de la regla
    2b. Si NO hay match          → llama a ai_service.process_message()
    3. Merge de resultados       → la regla puede overridear solo parcialmente
    4. Persistir + retornar

Almacenamiento actual: lista en memoria (in-process).
Para migrar a DB: reemplazar la lista por llamadas al repositorio/ORM.
"""

import uuid
import logging
from typing import List

from app.models.message import Message
from app.schemas.message import MessageCreate, MessageResponse
from app.services.ai_service import process_message as ai_process
from app.services.rule_engine import apply_rules

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# "Base de datos" en memoria
# Al integrar una DB real, este store se elimina y se usa un repositorio.
# ---------------------------------------------------------------------------
_message_store: List[Message] = []


def _resolve_result(content: str) -> tuple[str, str, bool]:
    """
    Determina la clasificacion y respuesta final para un mensaje.

    Estrategia:
        1. Verifica si alguna regla coincide (rule_engine)
        2. Si la regla tiene AMBOS campos → resultado completo, no llama a AI
        3. Si la regla tiene UN campo     → AI rellena el campo faltante
        4. Si no hay regla               → AI resuelve todo

    Returns:
        Tuple (classification, response, rule_matched)
    """
    rule_result = apply_rules(content)
    ai_result = None

    if rule_result:
        classification = rule_result.get("classification")
        response = rule_result.get("response")

        # Si la regla es completa, no necesitamos llamar al AI
        if classification and response:
            logger.info("Regla coincidio. Clasificacion: %s (sin AI)", classification)
            return classification, response, True

        # La regla es parcial → el AI rellena el campo faltante
        logger.info("Regla parcial. Complementando con AI...")
        ai_result = ai_process(content)
        classification = classification or ai_result["classification"]
        response = response or ai_result["response"]
        return classification, response, True

    # Sin regla → AI resuelve todo
    logger.info("Sin regla coincidente. Procesando con AI...")
    ai_result = ai_process(content)
    return ai_result["classification"], ai_result["response"], False


def create_message(payload: MessageCreate) -> MessageResponse:
    """
    Crea un nuevo mensaje, lo procesa y lo persiste en memoria.

    Flujo:
        1. _resolve_result() decide entre reglas y/o AI
        2. Construye el modelo Message con los resultados
        3. Persiste en el store interno
        4. Retorna MessageResponse completo

    Args:
        payload: Datos validados del mensaje (contenido).

    Returns:
        MessageResponse con id, timestamp, classification y response.
    """
    classification, response, rule_matched = _resolve_result(payload.content)

    new_message = Message(
        id=str(uuid.uuid4()),
        content=payload.content,
        classification=classification,
        ai_response=response,
        rule_matched=rule_matched,
    )
    _message_store.append(new_message)

    return MessageResponse(
        id=new_message.id,
        content=new_message.content,
        created_at=new_message.created_at,
        classification=new_message.classification,
        response=new_message.ai_response,
        rule_matched=new_message.rule_matched,
    )


def get_all_messages() -> List[MessageResponse]:
    """
    Recupera todos los mensajes almacenados con sus metadatos.

    Returns:
        Lista de MessageResponse (puede estar vacia).
    """
    return [
        MessageResponse(
            id=msg.id,
            content=msg.content,
            created_at=msg.created_at,
            classification=msg.classification,
            response=msg.ai_response,
            rule_matched=msg.rule_matched,
        )
        for msg in _message_store
    ]