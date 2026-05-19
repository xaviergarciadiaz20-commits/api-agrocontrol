from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.models import Animal, Finca, Usuario
from app.schemas.schemas import AnimalCreate, AnimalUpdate, AnimalOut
from app.auth import get_current_user

router = APIRouter(prefix="/api/animales", tags=["Animales"])


def verificar_finca(db: Session, finca_id: int, usuario_id: int):
    finca = (
        db.query(Finca)
        .filter(Finca.id == finca_id, Finca.usuario_id == usuario_id)
        .first()
    )
    if not finca:
        raise HTTPException(status_code=404, detail="Finca no encontrada o no autorizada")
    return finca


@router.get("/", response_model=List[AnimalOut])
def listar_animales(
    finca_id: Optional[int] = Query(None),
    tipo: Optional[str] = Query(None),
    estado: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    fincas_ids = [f.id for f in db.query(Finca.id).filter(Finca.usuario_id == usuario.id)]
    query = db.query(Animal).filter(Animal.finca_id.in_(fincas_ids))

    if finca_id:
        query = query.filter(Animal.finca_id == finca_id)
    if tipo:
        query = query.filter(Animal.tipo == tipo)
    if estado:
        query = query.filter(Animal.estado == estado)

    return query.order_by(Animal.created_at.desc()).all()


@router.get("/{animal_id}", response_model=AnimalOut)
def obtener_animal(
    animal_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    fincas_ids = [f.id for f in db.query(Finca.id).filter(Finca.usuario_id == usuario.id)]
    animal = (
        db.query(Animal)
        .filter(Animal.id == animal_id, Animal.finca_id.in_(fincas_ids))
        .first()
    )
    if not animal:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    return animal


@router.get("/codigo/{codigo}", response_model=AnimalOut)
def obtener_por_codigo(
    codigo: str,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    fincas_ids = [f.id for f in db.query(Finca.id).filter(Finca.usuario_id == usuario.id)]
    animal = (
        db.query(Animal)
        .filter(Animal.codigo == codigo, Animal.finca_id.in_(fincas_ids))
        .first()
    )
    if not animal:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    return animal


@router.post("/", response_model=AnimalOut, status_code=status.HTTP_201_CREATED)
def crear_animal(
    data: AnimalCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    verificar_finca(db, data.finca_id, usuario.id)

    if db.query(Animal).filter(Animal.codigo == data.codigo).first():
        raise HTTPException(status_code=400, detail="El código ya existe")

    animal = Animal(**data.model_dump())
    db.add(animal)
    db.commit()
    db.refresh(animal)
    return animal


@router.put("/{animal_id}", response_model=AnimalOut)
def actualizar_animal(
    animal_id: int,
    data: AnimalUpdate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    fincas_ids = [f.id for f in db.query(Finca.id).filter(Finca.usuario_id == usuario.id)]
    animal = (
        db.query(Animal)
        .filter(Animal.id == animal_id, Animal.finca_id.in_(fincas_ids))
        .first()
    )
    if not animal:
        raise HTTPException(status_code=404, detail="Animal no encontrado")

    update_data = data.model_dump(exclude_unset=True)
    if "finca_id" in update_data:
        verificar_finca(db, update_data["finca_id"], usuario.id)

    for key, value in update_data.items():
        setattr(animal, key, value)

    db.commit()
    db.refresh(animal)
    return animal


@router.delete("/{animal_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_animal(
    animal_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    fincas_ids = [f.id for f in db.query(Finca.id).filter(Finca.usuario_id == usuario.id)]
    animal = (
        db.query(Animal)
        .filter(Animal.id == animal_id, Animal.finca_id.in_(fincas_ids))
        .first()
    )
    if not animal:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    db.delete(animal)
    db.commit()
