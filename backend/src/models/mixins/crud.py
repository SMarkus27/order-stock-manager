from typing import Self, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session


class CRUDMixin:
    __abstract__ = True

    @classmethod
    def create(
        cls: type[Self], session: Session, auto_commit: bool = True, **kwargs: dict
    ) -> Self:

        try:
            instance = cls(**kwargs)
            session.add(instance)
            if auto_commit:
                session.commit()
                session.refresh(instance)
            return instance
        except Exception as e:
            session.rollback()
            raise e

    @classmethod
    def get(cls: type[Self], session: Session, id: int) -> Self | None:

        return session.get(cls, id)

    @classmethod
    def get_by_external_id_str(
        cls: type[Self], session: Session, external_id_str: str
    ) -> Self | None:
        query = select(cls).where(cls.external_id_str == external_id_str)
        return session.execute(query).scalar_one_or_none()

    def update(
        self: Self, session: Session, auto_commit: bool = False, **kwargs: dict
    ) -> Self:
        for key, value in kwargs.items():
            if not isinstance(value, dict):
                setattr(self, key, value)
            else:
                relation = getattr(self, key)
                if isinstance(relation, CRUDMixin):
                    relation.update(auto_commit=False, **value)

        if auto_commit:
            session.commit()
            session.refresh(self)
        return self

    def delete(
        self: Self,
        session: Session,
        target: Self | None = None,
        auto_commit: bool = True,
    ) -> Self:
        try:
            target = target or self
            session.delete(target)
            if auto_commit:
                session.commit()
            return target
        except Exception as e:
            session.rollback()
            raise e

    @classmethod
    def all(cls: type[Self], session: Session) -> Sequence["CRUDMixin"]:
        stmt = select(cls)
        return session.execute(stmt).scalars().all()
