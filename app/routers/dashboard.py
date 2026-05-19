from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func as sql_func
from app.database import get_db
from app.models.models import Animal, Finca, Usuario
from app.schemas.schemas import DashboardStats
from app.auth import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardStats)
def obtener_estadisticas(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    fincas_ids = [f.id for f in db.query(Finca.id).filter(Finca.usuario_id == usuario.id)]
    animales = db.query(Animal).filter(Animal.finca_id.in_(fincas_ids))

    total = animales.count()
    saludables = animales.filter(Animal.estado.in_(["Saludable", "Vacunado"])).count()
    enfermos = animales.filter(Animal.estado == "Enfermo").count()
    en_tratamiento = animales.filter(Animal.estado == "En tratamiento").count()
    vacunados = animales.filter(Animal.vacunado == 1).count()

    peso_prom = db.query(sql_func.avg(Animal.peso)).filter(
        Animal.finca_id.in_(fincas_ids)
    ).scalar() or 0

    cobertura = (vacunados / total * 100) if total > 0 else 0

    return DashboardStats(
        total_animales=total,
        total_fincas=len(fincas_ids),
        saludables=saludables,
        enfermos=enfermos,
        en_tratamiento=en_tratamiento,
        vacunados=vacunados,
        peso_promedio=round(float(peso_prom), 2),
        cobertura_vacunacion=round(cobertura, 1),
    )
