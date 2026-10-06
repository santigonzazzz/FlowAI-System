"""
Punto de entrada de la aplicacion FastAPI.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routes import health_router, messages_router

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# ---------------------------------------------------------------------------
# CORS — origenes configurables por entorno (settings.CORS_ORIGINS)
# Local: frontend Vite (5173). Produccion: dominio de Netlify, etc.
# Con "*" se desactivan las credenciales (no son compatibles con wildcard).
# ---------------------------------------------------------------------------
_origins = settings.cors_origin_list
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials="*" not in _origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(health_router)
app.include_router(messages_router)

@app.on_event("startup")
async def on_startup() -> None:
    pass

@app.on_event("shutdown")
async def on_shutdown() -> None:
    pass