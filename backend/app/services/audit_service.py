from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def create_audit_log(
    db: Session,
    username: str,
    method: str,
    endpoint: str,
    action: str,
    status_code: int
):

    log = AuditLog(
        username=username,
        method=method,
        endpoint=endpoint,
        action=action,
        status_code=status_code
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log