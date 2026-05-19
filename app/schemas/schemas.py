from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ─── AUTH / USUARIOS ─────────────────────────────

class UsuarioRegistro(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    tipo: str = "ganadero"
    telefono: Optional[str] = None


class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str


class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: str
    tipo: str
    telefono: Optional[str]
    activo: bool                    # ← era int; la columna PG es BOOLEAN
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioOut


# ─── FINCAS ──────────────────────────────────────

class FincaCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=150)
    ubicacion: Optional[str] = None
    departamento: Optional[str] = None
    hectareas: float = 0
    telefono: Optional[str] = None
    color: str = "#1b5e20"


class FincaUpdate(BaseModel):
    nombre: Optional[str] = None
    ubicacion: Optional[str] = None
    departamento: Optional[str] = None
    hectareas: Optional[float] = None
    telefono: Optional[str] = None
    color: Optional[str] = None


class FincaOut(BaseModel):
    id: int
    nombre: str
    ubicacion: Optional[str]
    departamento: Optional[str]
    hectareas: float
    telefono: Optional[str]
    color: str
    usuario_id: int
    created_at: datetime
    total_animales: Optional[int] = 0

    class Config:
        from_attributes = True


# ─── ANIMALES ────────────────────────────────────

class AnimalCreate(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=50)
    tipo: str = Field(..., max_length=50)
    raza: Optional[str] = None
    peso: float = 0
    edad_meses: int = 0
    estado: str = "Saludable"
    sexo: Optional[str] = None
    origen: Optional[str] = None
    fecha_ingreso: Optional[str] = None
    cond_reproductiva: Optional[str] = None
    vacunado: bool = False              # ← era int = 0; PG rechaza int en BOOLEAN
    observaciones: Optional[str] = None
    finca_id: int


class AnimalUpdate(BaseModel):
    tipo: Optional[str] = None
    raza: Optional[str] = None
    peso: Optional[float] = None
    edad_meses: Optional[int] = None
    estado: Optional[str] = None
    sexo: Optional[str] = None
    origen: Optional[str] = None
    fecha_ingreso: Optional[str] = None
    cond_reproductiva: Optional[str] = None
    vacunado: Optional[bool] = None     # ← era Optional[int]
    observaciones: Optional[str] = None
    finca_id: Optional[int] = None


class AnimalOut(BaseModel):
    id: int
    codigo: str
    tipo: str
    raza: Optional[str]
    peso: float
    edad_meses: int
    estado: str
    sexo: Optional[str]
    origen: Optional[str]
    fecha_ingreso: Optional[str]
    cond_reproductiva: Optional[str]
    vacunado: bool                      # ← era int
    observaciones: Optional[str]
    finca_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ─── VACUNACIONES ────────────────────────────────

class VacunacionCreate(BaseModel):
    animal_codigo: str
    vacuna: str = Field(..., max_length=150)
    fecha: Optional[str] = None
    proxima_fecha: Optional[str] = None
    veterinario: Optional[str] = None
    lote: Optional[str] = None
    estado: str = "Al día"


class VacunacionUpdate(BaseModel):
    vacuna: Optional[str] = None
    fecha: Optional[str] = None
    proxima_fecha: Optional[str] = None
    veterinario: Optional[str] = None
    lote: Optional[str] = None
    estado: Optional[str] = None


class VacunacionOut(BaseModel):
    id: int
    animal_codigo: str
    vacuna: str
    fecha: Optional[str]
    proxima_fecha: Optional[str]
    veterinario: Optional[str]
    lote: Optional[str]
    estado: str
    created_at: datetime

    class Config:
        from_attributes = True


# ─── DASHBOARD / ESTADÍSTICAS ────────────────────

class DashboardStats(BaseModel):
    total_animales: int
    total_fincas: int
    saludables: int
    enfermos: int
    en_tratamiento: int
    vacunados: int
    peso_promedio: float
    cobertura_vacunacion: float
