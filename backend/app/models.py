from datetime import datetime
from sqlalchemy import String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Shot(Base):
    __tablename__ = "shots"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[str | None] = mapped_column(String(1000))
    status: Mapped[str] = mapped_column(String(20), default="todo", server_default="todo")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
