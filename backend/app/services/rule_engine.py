"""
Motor de reglas de automatizacion — rule_engine.py

Simula un motor tipo Zapier / Make simplificado.
Cada regla define una condicion (keyword) y acciones opcionales
(override de clasificacion y/o respuesta personalizada).

Arquitectura para escalar:
  - Ahora: reglas hardcodeadas en lista Python
  - Despues: cargar reglas desde DB con SQLAlchemy
    (solo cambia _load_rules(), el resto del modulo no toca nada)

Orden de evaluacion:
  - Las reglas se evaluan en orden de lista
  - Gana la PRIMERA que coincida (early return)
  - Para cambiar prioridad: reordenar la lista o agregar campo "priority"
"""

from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Modelo de Regla
# ---------------------------------------------------------------------------


@dataclass
class Rule:
    """
    Define una regla de automatizacion.

    Campos:
        keyword:                 Palabra clave a buscar en el mensaje (case-insensitive).
        classification_override: Si se define, sobreescribe la clasificacion del AI.
        custom_response:         Si se define, sobreescribe la respuesta del AI.
        description:             Documentacion interna de la regla (no afecta logica).

    Logica de override:
        - Si ambos campos estan definidos  → se usa la regla completa, se omite el AI.
        - Si solo uno esta definido        → el AI rellena el campo faltante.
        - Si ninguno esta definido         → la regla coincide pero no hace nada util.
    """

    keyword: str
    classification_override: Optional[str] = None   # "hot" | "warm" | "cold"
    custom_response: Optional[str] = None
    description: str = ""


# ---------------------------------------------------------------------------
# Reglas en memoria (futura tabla en DB)
#
# Para migrar a DB:
#   1. Crear modelo SQLAlchemy Rule con los mismos campos
#   2. Reemplazar esta lista por una consulta:
#      SELECT * FROM rules ORDER BY priority ASC
#   3. La funcion apply_rules() no cambia
# ---------------------------------------------------------------------------


def _load_rules() -> list[Rule]:
    """
    Carga las reglas activas del sistema.

    NOTE: Reemplazar el contenido de esta funcion por una query a DB
    cuando se migre. La firma y el tipo de retorno NO cambian.
    """
    return [
        # ── Reglas HOT (alta intencion de compra) ─────────────────────────
        Rule(
            keyword="precio",
            classification_override="hot",
            custom_response=(
                "Te comparto informacion de precios de inmediato. "
                "Nuestros planes arrancan desde $29/mes e incluyen automatizacion ilimitada. "
                "Un asesor te enviara una cotizacion personalizada en menos de 10 minutos."
            ),
            description="Detecta solicitudes directas de precio",
        ),
        Rule(
            keyword="cotizacion",
            classification_override="hot",
            custom_response=(
                "Con gusto te preparamos una cotizacion a la medida. "
                "Uno de nuestros asesores te contactara en los proximos minutos "
                "con un plan adaptado a las necesidades de tu negocio."
            ),
            description="Detecta solicitudes de cotizacion",
        ),
        Rule(
            keyword="contratar",
            classification_override="hot",
            custom_response=(
                "Excelente decision! Para iniciar el proceso de contratacion "
                "un asesor te contactara hoy mismo para guiarte paso a paso. "
                "Tambien puedes iniciar directamente en flowai.com/start."
            ),
            description="Detecta intencion directa de contratar",
        ),

        # ── Reglas WARM (interes moderado) ────────────────────────────────
        Rule(
            keyword="demo",
            classification_override="warm",
            custom_response=(
                "Con mucho gusto! Tenemos demos en vivo todos los martes y jueves. "
                "Tambien puedes ver nuestra demo grabada en flowai.com/demo "
                "o solicitar una sesion privada con nuestro equipo."
            ),
            description="Detecta solicitud de demostracion",
        ),
        Rule(
            keyword="prueba gratis",
            classification_override="warm",
            custom_response=(
                "Tenemos un trial gratuito de 14 dias sin necesidad de tarjeta de credito. "
                "Registrate en flowai.com/trial y empieza a automatizar hoy mismo."
            ),
            description="Detecta interes en trial gratuito",
        ),
        Rule(
            keyword="integraciones",
            classification_override="warm",
            custom_response=(
                "FlowAI se integra con mas de 200 aplicaciones: "
                "WhatsApp, Slack, HubSpot, Salesforce, Google Sheets y muchas mas. "
                "Te puedo decir si tenemos la integracion especifica que necesitas."
            ),
            description="Detecta consulta sobre integraciones",
        ),

        # ── Reglas COLD (manejo especial) ─────────────────────────────────
        Rule(
            keyword="queja",
            classification_override="cold",
            custom_response=(
                "Lamentamos escuchar eso y queremos resolverlo de inmediato. "
                "Por favor envianos los detalles a soporte@flowai.com "
                "y un agente te respondera en menos de 2 horas."
            ),
            description="Deriva quejas al equipo de soporte",
        ),
        Rule(
            keyword="cancelar",
            classification_override="cold",
            custom_response=(
                "Entendemos. Antes de proceder, nos gustaria conocer tu experiencia "
                "para poder mejorar. Un asesor te contactara para escucharte "
                "y, si es posible, encontrar una solucion que funcione para ti."
            ),
            description="Manejo de solicitudes de cancelacion",
        ),
    ]


# ---------------------------------------------------------------------------
# Motor de evaluacion
# ---------------------------------------------------------------------------


def apply_rules(content: str) -> dict | None:
    """
    Evalua el mensaje contra todas las reglas activas.

    Logica:
        1. Normaliza el contenido a minusculas
        2. Itera las reglas en orden (primera coincidencia gana)
        3. Si hay match: construye y retorna el dict de overrides
        4. Si no hay match: retorna None (el AI se encarga)

    Args:
        content: Texto del mensaje del cliente.

    Returns:
        dict con claves opcionales:
            - "classification": valor override
            - "response": respuesta personalizada
        None si ninguna regla coincide.
    """
    text = content.lower()
    rules = _load_rules()

    for rule in rules:
        if rule.keyword.lower() in text:
            overrides: dict = {}

            if rule.classification_override:
                overrides["classification"] = rule.classification_override

            if rule.custom_response:
                overrides["response"] = rule.custom_response

            # Solo retornar si hay al menos un override util
            if overrides:
                return overrides

    return None