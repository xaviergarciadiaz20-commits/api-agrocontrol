from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import Finca, Animal, Usuario
from app.schemas.schemas import FincaCreate, FincaUpdate, FincaOut
from app.auth import get_current_user

router = APIRouter(prefix="/api/fincas", tags=["Fincas"])


def finca_to_out(finca: Finca, db: Session) -> FincaOut:
    total = db.query(Animal).filter(Animal.finca_id == finca.id).count()
    data = FincaOut.model_validate(finca)
    data.total_animales = total
    return data


@router.get("/", response_model=List[FincaOut])
def listar_fincas(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    fincas = db.query(Finca).filter(Finca.usuario_id == usuario.id).all()
    return [finca_to_out(f, db) for f in fincas]


@router.get("/{finca_id}", response_model=FincaOut)
def obtener_finca(
    finca_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    finca = (
        db.query(Finca)
        .filter(Finca.id == finca_id, Finca.usuario_id == usuario.id)
        .first()
    )
    if not finca:
        raise HTTPException(status_code=404, detail="Finca no encontrada")
    return finca_to_out(finca, db)


@router.post("/", response_model=FincaOut, status_code=status.HTTP_201_CREATED)
def crear_finca(
    data: FincaCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    finca = Finca(**data.model_dump(), usuario_id=usuario.id)
    db.add(finca)
    db.commit()
    db.refresh(finca)
    return finca_to_out(finca, db)


@router.put("/{finca_id}", response_model=FincaOut)
def actualizar_finca(
    finca_id: int,
    data: FincaUpdate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    finca = (
        db.query(Finca)
        .filter(Finca.id == finca_id, Finca.usuario_id == usuario.id)
        .first()
    )
    if not finca:
        raise HTTPException(status_code=404, detail="Finca no encontrada")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(finca, key, value)

    db.commit()
    db.refresh(finca)
    return finca_to_out(finca, db)


@router.delete("/{finca_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_finca(
    finca_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    finca = (
        db.query(Finca)
        .filter(Finca.id == finca_id, Finca.usuario_id == usuario.id)
        .first()
    )
    if not finca:
        raise HTTPException(status_code=404, detail="Finca no encontrada")
    db.delete(finca)
    db.commit()
