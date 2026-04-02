"""
Router de health — expone el endpoint GET /health.
Permite verificar que la API está activa (útil para load balancers y CI/CD).
"""

from fastapi import APIRouter
from app.schemas.health import HealthResponse

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Verifica que el servicio está activo y respondiendo.",
)
def health_check() -> HealthResponse:
    """Retorna el estado operativo de la API."""
    return HealthResponse(status="ok")
