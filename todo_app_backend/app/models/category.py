from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class CategoryORM(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(255))