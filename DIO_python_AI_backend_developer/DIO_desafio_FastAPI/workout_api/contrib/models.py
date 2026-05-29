from uuid import uuid4, UUID as py_UUID
from sqlalchemy import Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    id: Mapped[py_UUID] = mapped_column(Uuid, default=uuid4, nullable=False)