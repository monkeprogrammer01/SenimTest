from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from user.models.user import User
from auth.services.auth_service import get_current_user
from report.models.report import Report
from report.schemas.report import ReportCreate, ReportOut
from datetime import datetime, UTC
report_router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

@report_router.get("/", response_model=list[ReportOut])
def get_reports(currentUser: User = Depends(get_current_user), db: Session = Depends(get_db)):
    role = currentUser.role.value

    if role == "admin":
        reports = db.query(Report).all()
    elif role == "staff":
        reports = db.query(Report).filter(Report.user_id==currentUser.id).all()
    else:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail="Access denied for this role."
        )
    return reports

@report_router.post("/", response_model=ReportOut, status_code=status.HTTP_201_CREATED)
def create_report(data: ReportCreate, currentUser: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_report = Report(
        category = data.category,
        message = data.message,
        user_id = currentUser.id,
        created_at = datetime.now(UTC)
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report