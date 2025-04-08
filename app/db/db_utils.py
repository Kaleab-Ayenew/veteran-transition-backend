from sqlmodel import Session, select
from app.db.database import engine
from app.db import models
from typing import Union
def create_row(model, data: dict):
    new_data = model(**data)
    with Session(engine) as session:
        session.add(new_data)
        session.commit()
        session.refresh(new_data)
        return new_data

def filter_rows(model, filters: tuple):
    with Session(engine) as session:
        statement = select(model).filter(*filters)
        results = session.exec(statement).fetchall()
        return results

def get_one_row(model, filters: tuple):
    with Session(engine) as session:
        statement = select(model).filter(*filters)
        result = session.exec(statement).one_or_none()
        return result

def update_row(model, filters: tuple, data: dict):
    with Session(engine) as session:
        statement = select(model).filter(*filters)
        result = session.exec(statement).one()
        for key, value in data.items():
            setattr(result, key, value)
        session.add(result)
        session.commit()
        session.refresh(result)
        return result

def delete_row(model, filters):
    with Session(engine) as session:
        statement = select(model).filter(*filters)
        result = session.exec(statement).one()
        session.delete(result)
        session.commit()
        return result
