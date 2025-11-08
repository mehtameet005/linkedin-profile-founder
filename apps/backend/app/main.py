from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import sentry_sdk

from app.core.config import settings
from app.db.session import engine
from app.db.base import Base
from app.api.routes import (
    auth,
    jobs,
    icps,
    personas,
    candidates,
    discovery,
    exports,
)


# Initialize Sentry
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
        traces_sample_rate=1.0 if settings.DEBUG else 0.1,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        # Create tables if they don't exist (for dev only)
        if settings.DEBUG:
            await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered LinkedIn profile discovery platform",
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["Jobs"])
app.include_router(icps.router, prefix="/api/icps", tags=["ICPs"])
app.include_router(personas.router, prefix="/api/personas", tags=["Personas"])
app.include_router(candidates.router, prefix="/api/candidates", tags=["Candidates"])
app.include_router(discovery.router, prefix="/api/discovery", tags=["Discovery"])
app.include_router(exports.router, prefix="/api/exports", tags=["Exports"])


@app.get("/")
async def root():
    return {
        "message": "LinkedIn Profile Finder API",
        "version": settings.APP_VERSION,
        "status": "operational",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
