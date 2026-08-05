from sqlalchemy.orm import Session

from app.models.decision import Decision


def save_decision(
    db: Session,
    agent_name,
    decision,
    reason,
    confidence,
    username=None
):

    new_decision = Decision(
        agent_name=agent_name,
        decision=decision,
        reason=reason,
        confidence=confidence,
        username=username
    )

    db.add(new_decision)
    db.commit()
    db.refresh(new_decision)

    return new_decision


def get_decision_history(
    db: Session,
    agent_name: str = None,
    decision: str = None,
    username: str = None,
    date_from=None,
    date_to=None,
    page: int = 1,
    page_size: int = 20
):
    """
    Returns a filtered, paginated slice of decision history plus the total
    matching count (for building pagination UI on the frontend).
    """

    query = db.query(Decision)

    if agent_name:
        query = query.filter(Decision.agent_name == agent_name)

    if decision:
        query = query.filter(Decision.decision == decision)

    if username:
        query = query.filter(Decision.username == username)

    if date_from:
        query = query.filter(Decision.created_at >= date_from)

    if date_to:
        query = query.filter(Decision.created_at <= date_to)

    total = query.count()

    page = max(page, 1)
    page_size = max(1, min(page_size, 200))

    results = (
        query
        .order_by(Decision.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "results": results
    }
