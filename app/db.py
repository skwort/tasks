import os
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import String, Integer
from typing import Optional


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(String(10))
    category_rank: Mapped[int] = mapped_column(Integer())
    title: Mapped[Optional[str]] = mapped_column(String(64))
    body: Mapped[Optional[str]] = mapped_column(String(256))

    def to_dict(self) -> dict:
        class_dict = {}
        class_attrs = [k for k in dir(self)]
        for attr in class_attrs:
            # Filter out private attributes
            if attr.startswith("_"):
                continue
            elif attr == "metadata" or attr == "registry":
                continue
            elif callable(getattr(self, attr, None)):
                continue

            class_dict[attr] = getattr(self, attr, None)

        return class_dict

    def __repr__(self) -> str:
        return (
            f"Task(\n"
            f"    id={self.id!r},\n"
            f"    category={self.category!r},\n"
            f"    category_rank={self.category_rank!r},\n"
            f"    title={self.title!r}\n"
            f")"
        )


def setup_db(db_uri, echo=True):
    engine = create_engine(db_uri, echo=echo)
    session = scoped_session(sessionmaker(bind=engine))

    if not os.path.exists(db_uri.split("/")[-1]):
        Task.metadata.create_all(engine)

    return engine, session
