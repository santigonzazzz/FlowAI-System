"""
Servicio de procesamiento de mensajes con IA real (Groq via OpenAI SDK).

Arquitectura:
  1. Groq como motor principal (llama-3.3-70b-versatile)
  2. Structured Output con Pydantic para garantizar formato exacto
  3. Fallback automatico a clasificacion por palabras clave si Groq no esta disponible

Integracion Groq:
  - OpenAI Python SDK apuntando a https://api.groq.com/openai/v1
  - Compatible 100% con la API de OpenAI (base_url diferente, misma interfaz)
  - Usa chat.completions.create con response_format json_object
  - El resultado se valida con Pydantic antes de retornar
"""

import json
import logging
from typing import Literal

from openai import OpenAI, OpenAIError
from pydantic import BaseModel, field_validator

from app.config import get_settings

logger = logging.getLogger(__name__)

# -- Tipos -------------------------------------------------------------------

Classification = Literal["hot", "warm", "cold"]

# -- Schema de respuesta estructurada (Pydantic) -----------------------------


class AIResult(BaseModel):
    """
    Estructura exacta que Groq debe retornar en JSON.
    Pydantic valida que classification sea uno de los tres valores permitidos
    y que response sea un string no vacio.
    """

    classification: Classification
    response: str

    @field_validator("classification")
    @classmethod
    def classification_must_be_valid(cls, v: str) -> str:
        allowed = {"hot", "warm", "cold"}
        if v not in allowed:
            raise ValueError(f"classification debe ser uno de {allowed}, recibido: {v!r}")
        return v


# -- System prompt -----------------------------------------------------------

_SYSTEM_PROMPT = """Eres un asistente de atencion al cliente de FlowAI, una plataforma de automatizacion con IA.

Tu tarea al recibir el mensaje de un cliente es:

1. CLASIFICAR la intencion del cliente en UNA de estas tres categorias:
   - "hot": el cliente muestra intencion clara de compra (menciona precio, cotizacion, comprar, adquirir, contratar, cuanto cuesta, info sobre planes, disponibilidad)
   - "warm": el cliente muestra interes moderado (quiere saber mas, pide detalles, pregunta como funciona, expresa interes)
   - "cold": cualquier otro caso (saludo generico, queja, mensaje de prueba, off-topic)

2. GENERAR una respuesta apropiada, breve (max 2 oraciones) y en espanol, acorde a la clasificacion:
   - hot: orientada a cerrar la venta, menciona que un asesor lo contactara
   - warm: informativa y amigable, invita a conocer mas
   - cold: cortés y general, deja la puerta abierta

IMPORTANTE: Responde UNICAMENTE con un objeto JSON valido con exactamente estas dos claves:
{
  "classification": "hot" | "warm" | "cold",
  "response": "texto de respuesta al cliente"
}
No agregues ninguna explicacion, texto adicional ni formato markdown fuera del JSON."""

# -- Fallback (palabras clave) -----------------------------------------------

_HOT_KEYWORDS = ["precio", "precios", "comprar", "compra", "cotizacion", "cuanto cuesta",
                  "info", "informacion", "adquirir", "contratar", "disponible", "oferta"]
_WARM_KEYWORDS = ["me interesa", "interesado", "quiero saber", "detalles", "mas informacion",
                  "cuentame", "explicame", "como funciona", "caracteristicas"]
_FALLBACK_RESPONSES: dict[str, str] = {
    "hot": "Excelente! Un asesor se pondra en contacto contigo pronto con una cotizacion personalizada.",
    "warm": "Gracias por tu interes! FlowAI automatiza la atencion al cliente con IA. Te cuento mas detalles.",
    "cold": "Hola! Gracias por contactarnos. Estamos aqui para ayudarte en lo que necesites.",
}


def _fallback_classify(content: str) -> Classification:
    text = content.lower()
    if any(kw in text for kw in _HOT_KEYWORDS):
        return "hot"
    if any(kw in text for kw in _WARM_KEYWORDS):
        return "warm"
    return "cold"


def _fallback_process(content: str) -> dict:
    classification = _fallback_classify(content)
    return {"classification": classification, "response": _FALLBACK_RESPONSES[classification]}


# -- Motor principal (Groq) --------------------------------------------------


def _groq_process(content: str) -> dict:
    """
    Llama a Groq usando el cliente OpenAI con base_url apuntando a Groq.

    Usa response_format={"type": "json_object"} para forzar JSON valido.
    Luego valida la estructura con Pydantic (AIResult).

    Raises:
        OpenAIError: si la API falla (red, clave invalida, rate limit, etc.)
        ValueError: si el JSON no tiene el formato esperado
    """
    settings = get_settings()

    client = OpenAI(
        api_key=settings.GROQ_API_KEY,
        base_url=settings.GROQ_BASE_URL,
    )

    completion = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": content},
        ],
        response_format={"type": "json_object"},
        temperature=0.3,          # Determinismo alto para clasificacion consistente
        max_tokens=200,           # La respuesta es corta, no necesitamos mas
    )

    raw_json = completion.choices[0].message.content
    data = json.loads(raw_json)
    result = AIResult(**data)     # Validacion Pydantic

    return result.model_dump()


# -- API publica del servicio ------------------------------------------------


def process_message(content: str) -> dict:
    """
    Punto de entrada unico. Procesa un mensaje y retorna clasificacion + respuesta.

    Flujo:
        1. Intenta _groq_process() con Groq real
        2. Si falla (sin API key, error de red, limite de rate), usa _fallback_process()

    Args:
        content: Texto del mensaje del cliente.

    Returns:
        dict con:
            - classification: "hot" | "warm" | "cold"
            - response: texto de respuesta automatica
    """
    settings = get_settings()

    if not settings.GROQ_API_KEY:
        logger.warning("GROQ_API_KEY no configurado. Usando fallback por palabras clave.")
        return _fallback_process(content)

    try:
        result = _groq_process(content)
        logger.info("Groq proceso el mensaje. Clasificacion: %s", result["classification"])
        return result

    except (OpenAIError, ValueError, json.JSONDecodeError) as exc:
        logger.error("Error al llamar a Groq: %s. Usando fallback.", exc)
        return _fallback_process(content)
