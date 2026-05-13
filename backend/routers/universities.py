from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List

from database import get_db
import crud
import schemas

router = APIRouter(prefix="/api/universities", tags=["universities"])


@router.get("", response_model=schemas.UniversitiesResponse)
def list_universities(
    country: Optional[str] = None,
    specialty: Optional[str] = None,
    search: Optional[str] = None,
    page: int = 1,
    limit: int = 12,
    db: Session = Depends(get_db),
):
    skip = (page - 1) * limit
    items, total = crud.get_universities(db, country, specialty, search, skip, limit)
    pages = max(1, (total + limit - 1) // limit)
    return schemas.UniversitiesResponse(items=items, total=total, page=page, pages=pages)


@router.get("/countries", response_model=List[str])
def list_countries(db: Session = Depends(get_db)):
    return crud.get_countries(db)


@router.get("/specialties", response_model=List[schemas.SpecialtyOut])
def list_specialties(db: Session = Depends(get_db)):
    return crud.get_specialties(db)


@router.get("/{university_id}", response_model=schemas.UniversityOut)
def get_university(university_id: int, db: Session = Depends(get_db)):
    uni = crud.get_university(db, university_id)
    if not uni:
        raise HTTPException(status_code=404, detail="University not found")
    return uni
