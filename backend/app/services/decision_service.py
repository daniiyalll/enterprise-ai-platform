from sqlalchemy.orm import Session

from app.models.decision import Decision


def save_decision(
    db: Session,
    agent_name,
    decision,
    reason,
    confidence
):

    new_decision = Decision(
        agent_name=agent_name,
        decision=decision,
        reason=reason,
        confidence=confidence
    )

    db.add(new_decision)
    db.commit()
    db.refresh(new_decision)

    return new_decision


def get_decision_history(db: Session, limit: int = 50):

    return (
        db.query(Decision)
        .order_by(Decision.id.desc())
        .limit(limit)
        .all()
    )
