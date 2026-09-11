from typing import Optional, List
from sqlalchemy.orm import Session

from . import models, schemas


def create_advertisement(db: Session, data: schemas.AdvertisementCreate) -> models.Advertisement:
    obj = models.Advertisement(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_advertisement(db: Session, adv_id: int) -> Optional[models.Advertisement]:
    return db.get(models.Advertisement, adv_id)


def update_advertisement(
    db: Session, adv_id: int, data: schemas.AdvertisementUpdate
) -> Optional[models.Advertisement]:
    obj = db.get(models.Advertisement, adv_id)
    if obj is None:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_advertisement(db: Session, adv_id: int) -> bool:
    obj = db.get(models.Advertisement, adv_id)
    if obj is None:
        return False
    db.delete(obj)
    db.commit()
    return True


def search_advertisements(
    db: Session,
    title: Optional[str] = None,
    author: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
) -> List[models.Advertisement]:
    query = db.query(models.Advertisement)
    if title:
        query = query.filter(models.Advertisement.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(models.Advertisement.author.ilike(f"%{author}%"))
    if min_price is not None:
        query = query.filter(models.Advertisement.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Advertisement.price <= max_price)
    return query.order_by(models.Advertisement.created_at.desc()).all()