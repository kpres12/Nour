from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1 import auth, sources, ingest, entities, narratives, signals, playbooks

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(sources.router, prefix=settings.API_V1_STR)
app.include_router(ingest.router, prefix=settings.API_V1_STR)
app.include_router(entities.router, prefix=settings.API_V1_STR)
app.include_router(narratives.router, prefix=settings.API_V1_STR)
app.include_router(signals.router, prefix=settings.API_V1_STR)
app.include_router(playbooks.router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {"message": "Welcome to Nour - Narrative Intelligence Platform"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "nour-backend"}
