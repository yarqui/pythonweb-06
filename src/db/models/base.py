from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs

metadata_obj = MetaData()


class MinimalBase(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    metadata = metadata_obj


class IDOrmModel(MinimalBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
