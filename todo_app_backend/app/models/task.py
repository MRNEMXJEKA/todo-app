from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class TaskORM(Base):
    __tablename__ = "tasks"

    title: Mapped[str] = mapped_column(String(255))
    completed: Mapped[bool] = mapped_column(default=False)
