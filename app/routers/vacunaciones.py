from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.models import Vacunacion, Animal, Finca, Usuario
from app.schemas.schemas import VacunacionCreate, VacunacionUpdate, VacunacionOut
from app.auth import get_current_user

router = APIRouter(prefix="/api/vacunaciones", tags=["Vacunaciones"])


def animal_del_usuario(db: Session, codigo: str, usuario_id: int) -> Animal:
    fincas_ids = [f.id for f in db.query(Finca.id).filter(Finca.usuario_id == usuario_id)]
    animal = (
        db.query(Animal)
        .filter(Animal.codigo == codigo, Animal.finca_id.in_(fincas_ids))
        .first()
    )
    if not animal:
        raise HTTPException(status_code=404, detail="Animal no encontrado o no autorizado")
    return animal


@router.get("/", response_model=List[VacunacionOut])
def listar_vacunaciones(
    animal_codigo: Optional[str] = Query(None),
    estado: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    fincas_ids = [f.id for f in db.query(Finca.id).filter(Finca.usuario_id == usuario.id)]
    codigos = [
        a.codigo
        for a in db.query(Animal.codigo).filter(Animal.finca_id.in_(fincas_ids))
    ]

    query = db.query(Vacunacion).filter(Vacunacion.animal_codigo.in_(codigos))

    if animal_codigo:
        query = query.filter(Vacunacion.animal_codigo == animal_codigo)
    if estado:
        query = query.filter(Vacunacion.estado == estado)

    return query.order_by(Vacunacion.created_at.desc()).all()


@router.get("/{vacunacion_id}", response_model=VacunacionOut)
def obtener_vacunacion(
    vacunacion_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    vac = db.query(Vacunacion).filter(Vacunacion.id == vacunacion_id).first()
    if not vac:
        raise HTTPException(status_code=404, detail="Vacunación no encontrada")
    animal_del_usuario(db, vac.animal_codigo, usuario.id)
    return vac


@router.post("/", response_model=VacunacionOut, status_code=status.HTTP_201_CREATED)
def crear_vacunacion(
    data: VacunacionCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    animal_del_usuario(db, data.animal_codigo, usuario.id)

    vac = Vacunacion(**data.model_dump())
    db.add(vac)
    db.commit()
    db.refresh(vac)
    return vac


@router.put("/{vacunacion_id}", response_model=VacunacionOut)
def actualizar_vacunacion(
    vacunacion_id: int,
    data: VacunacionUpdate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    vac = db.query(Vacunacion).filter(Vacunacion.id == vacunacion_id).first()
    if not vac:
        raise HTTPException(status_code=404, detail="Vacunación no encontrada")
    animal_del_usuario(db, vac.animal_codigo, usuario.id)

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(vac, key, value)

    db.commit()
    db.refresh(vac)
    return vac


@router.delete("/{vacunacion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_vacunacion(
    vacunacion_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    vac = db.query(Vacunacion).filter(Vacunacion.id == vacunacion_id).first()
    if not vac:
        raise HTTPException(status_code=404, detail="Vacunación no encontrada")
    animal_del_usuario(db, vac.animal_codigo, usuario.id)
    db.delete(vac)
    db.commit()
