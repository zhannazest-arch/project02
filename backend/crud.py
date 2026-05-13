from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List, Tuple
import models


def get_universities(
    db: Session,
    country: Optional[str] = None,
    specialty: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 12,
) -> Tuple[List[models.University], int]:
    query = db.query(models.University)

    if country:
        query = query.filter(models.University.country == country)

    if specialty:
        query = query.join(models.University.specialties).filter(
            models.Specialty.name == specialty
        )

    if search:
        query = query.filter(
            or_(
                models.University.name.ilike(f"%{search}%"),
                models.University.city.ilike(f"%{search}%"),
                models.University.country.ilike(f"%{search}%"),
            )
        )

    total = query.count()
    items = (
        query.order_by(models.University.ranking.nulls_last())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return items, total


def get_university(db: Session, university_id: int) -> Optional[models.University]:
    return (
        db.query(models.University)
        .filter(models.University.id == university_id)
        .first()
    )


def get_countries(db: Session) -> List[str]:
    rows = (
        db.query(models.University.country)
        .distinct()
        .order_by(models.University.country)
        .all()
    )
    return [r[0] for r in rows]


def get_specialties(db: Session) -> List[models.Specialty]:
    return db.query(models.Specialty).order_by(models.Specialty.name).all()


def get_universities_by_filters(
    db: Session,
    countries: Optional[List[str]] = None,
    specialties: Optional[List[str]] = None,
    max_tuition: Optional[int] = None,
    limit: int = 5,
) -> List[models.University]:
    query = db.query(models.University)

    if countries:
        query = query.filter(models.University.country.in_(countries))

    if specialties:
        query = query.join(models.University.specialties).filter(
            models.Specialty.name.in_(specialties)
        )

    if max_tuition:
        query = query.filter(
            or_(
                models.University.tuition_min <= max_tuition,
                models.University.tuition_min.is_(None),
            )
        )

    return (
        query.order_by(models.University.ranking.nulls_last()).limit(limit).all()
    )
