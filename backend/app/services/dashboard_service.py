from sqlalchemy.orm import Session
from app.models.decision import Decision


def get_dashboard_stats(db: Session):

    total_decisions = db.query(Decision).count()

    total_approvals = db.query(Decision).filter(
        Decision.decision.in_(["approved", "passed"])
    ).count()

    total_rejections = db.query(Decision).filter(
        Decision.decision == "rejected"
    ).count()

    total_reviews_needed = db.query(Decision).filter(
        Decision.decision == "review_required"
    ).count()

    compliance_failures = db.query(Decision).filter(
        Decision.agent_name == "Compliance Agent",
        Decision.decision == "failed"
    ).count()

    document_rejections = db.query(Decision).filter(
        Decision.agent_name == "Document Agent",
        Decision.decision == "rejected"
    ).count()

    all_decisions = db.query(Decision).all()

    if len(all_decisions) > 0:
        average_confidence = round(
            sum(d.confidence for d in all_decisions) / len(all_decisions),
            2
        )
    else:
        average_confidence = 0

    return {
        "total_decisions": total_decisions,
        "total_approvals": total_approvals,
        "total_rejections": total_rejections,
        "total_reviews_needed": total_reviews_needed,
        "compliance_failures": compliance_failures,
        "document_rejections": document_rejections,
        "average_confidence": average_confidence
    }
