from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.routers import auth, fincas, animales, vacunaciones, dashboard

settings = get_settings()

app = FastAPI(
    title="AgroControl API",
    description="API REST para el Sistema de Gestión Ganadera AgroControl",
    version="1.0.0",
)

# ─── CORS ────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── ROUTERS ─────────────────────────────────────
app.include_router(auth.router)
app.include_router(fincas.router)
app.include_router(animales.router)
app.include_router(vacunaciones.router)
app.include_router(dashboard.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "app": "AgroControl API",
        "version": "1.0.0",
        "docs": "/docs",
    }
