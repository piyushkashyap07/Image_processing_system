# api/upload.py

from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import SessionLocal, get_db
from ..schemas import ProcessedImageResponse
from ..models import Product, Request
from ..celery_worker import process_images
import uuid
from datetime import datetime

router = APIRouter()

def create_request(db: Session, request_id: str) -> Request:
    db_request = Request(
        request_id=request_id,
        status="Pending",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

@router.post("/upload", response_model=ProcessedImageResponse)
def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    print("inside upload csv!!!")
    # Read CSV file
    try:
        contents = file.file.read().decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid CSV file.")

    # Process CSV contents (validate and save to database)
    lines = contents.splitlines()
    headers = lines[0].strip().split(",")
    if len(headers) != 3 or headers[0] != "S. No." or headers[1] != "Product Name " or headers[2] != "Input Image Urls":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid CSV format.")

    # Generate a unique request ID
    request_id = str(uuid.uuid4())

    # Create a new request entry
    db_request = create_request(db=db, request_id=request_id)

    # Skip header and process each line
    for line in lines[1:]:
        fields = line.strip().split(",")
        if len(fields) != 3:
            continue
        serial_number, product_name, input_image_urls = fields
        # Save to database (Example: Product table)
        db_product = Product(
            serial_number=serial_number,
            product_name=product_name,
            input_image_urls=input_image_urls,
            request_id=db_request.id
        )
        db.add(db_product)
    db.commit()

    # Trigger the Celery task to process images
    process_images.delay(request_id)

    return {"request_id": request_id}
