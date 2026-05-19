from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.routers import auth, fincas, animales, vacunaciones, dashboard
from app.database import engine, Base # <-- Agregado
from app.models import models # <-- Agregado para que SQLAlchemy reconozca los modelos

settings = get_settings()

# <-- Crea las tablas en PostgreSQL automáticamente si no existen
Base.metadata.create_all(bind=engine) 

app = FastAPI(
    title="AgroControl API",
    description="API REST para el Sistema de Gestión Ganadera AgroControl",
    version="1.0.0",
)

# ─── CORS ────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # <-- Permite cualquier origen (Render/Vercel/Local)
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
