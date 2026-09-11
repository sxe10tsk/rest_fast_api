from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Advertisement Service")


@app.post(
    "/advertisement",
    response_model=schemas.AdvertisementOut,
    status_code=status.HTTP_201_CREATED,
)
def create_advertisement(
    payload: schemas.AdvertisementCreate,
    db: Session = Depends(get_db),
):
    return crud.create_advertisement(db, payload)


@app.get("/advertisement", response_model=List[schemas.AdvertisementOut])
def search_advertisements(
    title: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    db: Session = Depends(get_db),
):
    return crud.search_advertisements(
        db, title=title, author=author, min_price=min_price, max_price=max_price
    )


@app.get("/advertisement/{advertisement_id}", response_model=schemas.AdvertisementOut)
def get_advertisement(advertisement_id: int, db: Session = Depends(get_db)):
    obj = crud.get_advertisement(db, advertisement_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return obj


@app.patch("/advertisement/{advertisement_id}", response_model=schemas.AdvertisementOut)
def update_advertisement(
    advertisement_id: int,
    payload: schemas.AdvertisementUpdate,
    db: Session = Depends(get_db),
):
    obj = crud.update_advertisement(db, advertisement_id, payload)
    if obj is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return obj


@app.delete("/advertisement/{advertisement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_advertisement(advertisement_id: int, db: Session = Depends(get_db)):
    success = crud.delete_advertisement(db, advertisement_id)
    if not success:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return None