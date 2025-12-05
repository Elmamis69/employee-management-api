from typing import Optional
from sqlalchemy.orm import Session # <- Correcto, no de sqlalchemy
from app.models.activity_log import ActivityLog
from app.models.user import User

def create_activity(
        db: Session,
        user: Optional[User],
        action: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        details: Optional[str] = None,
) -> ActivityLog:
    entry = ActivityLog(
        user_id = user.id if user else None,
        action = action,
        resource_type = resource_type,
        resource_id = str(resource_id) if resource_id is not None else None,
        details = details,
    )
    db.add(entry)
    return entry