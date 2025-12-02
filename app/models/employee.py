from typing import Optional

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base, TimestampMixin

class Employee(TimestampMixin, Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, index = True)
    first_name: Mapped[str] = mapped_column(String(100), nullable = False)
    last_name: Mapped[str] = mapped_column(String(100), nullable = False)
    email: Mapped[Optional[str]] = mapped_column(String(255), unique = True, index = True, nullable = True)
    department: Mapped[Optional[str]] = mapped_column(String(100), nullable = True)
    position: Mapped[Optional[str]] = mapped_column(String(100), nullable = True)
    is_active: Mapped[bool] = mapped_column(Boolean, default = True, nullable = False)
    hired_at: Mapped[Optional[Date]] = mapped_column(Date, nullable = True)

    # opcional: quien creo este empleado
    created_by_id: Mapped [Optional[int]] = mapped_column (
        Integer,
        ForeignKey("users.id", ondelete = "SET NULL"),
        nullable = True,
    )
    created_by = relationship("User", backref = "created_employees")