# api/status.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal, get_db
from ..schemas import StatusResponse
from ..models import Request

router = APIRouter()

@router.get("/status/{request_id}", response_model=StatusResponse)
def get_status(request_id: str, db: Session = Depends(get_db)):
    # Fetch the request by request_id
    db_request = db.query(Request).filter(Request.request_id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    return {"status": db_request.status}
