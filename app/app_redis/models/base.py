from sqlalchemy import Integer, DateTime, String, func
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import mapped_column, Mapped


@as_declarative()
class Base:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    @classmethod
    def table_name(cls):
        return cls.__tablename__

    @classmethod
    def schema_name(cls):
        return cls.__table_args__["schema"]
