# crud/ambiente.py
from sqlalchemy.orm import Session

from Trabalho_BD2.IntegrationApplication.integration_api.schemas.ambiente import Ambiente, AmbienteCreate


def get_ambiente(db: Session, ambiente_id: int):
    return db.query(Ambiente).filter(Ambiente.Id_Amb == ambiente_id).first()

def get_ambientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Ambiente).offset(skip).limit(limit).all()

def create_ambiente(db: Session, ambiente: AmbienteCreate):
    db_ambiente = Ambiente(**ambiente.dict())
    db.add(db_ambiente)
    db.commit()
    db.refresh(db_ambiente)
    return db_ambiente

def update_ambiente(db: Session, ambiente_id: int, ambiente: AmbienteCreate):
    db_ambiente = get_ambiente(db, ambiente_id)
    if db_ambiente:
        for key, value in ambiente.dict().items():
            setattr(db_ambiente, key, value)
        db.commit()
        db.refresh(db_ambiente)
    return db_ambiente

def delete_ambiente(db: Session, ambiente_id: int):
    db_ambiente = get_ambiente(db, ambiente_id)
    if db_ambiente:
        db.delete(db_ambiente)
        db.commit()
    return db_ambiente