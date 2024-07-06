from celery import Celery
import requests
from app.database import SessionLocal
from app import models

celery = Celery(__name__, broker="redis://localhost:6379/0")

@celery.task
def process_images(request_id: str):
    db: Session = SessionLocal()
    products = db.query(models.Product).filter(models.Product.request_id == request_id).all()

    for product in products:
        input_urls = product.input_image_urls.split(",")
        output_urls = []

        for url in input_urls:
            response = requests.get(url)
            image = response.content

            # Compress image (this is a placeholder; actual compression logic needed)
            compressed_image = image  # Replace with actual compression logic

            # Save compressed image to a storage service and get URL (placeholder logic)
            output_url = url.replace("public-image", "public-image-output")
            output_urls.append(output_url)

        product.output_image_urls = ",".join(output_urls)
        db.commit()

    # Update request status
    request = db.query(models.Request).filter(models.Request.request_id == request_id).first()
    request.status = "Completed"
    db.commit()
    db.close()

    
# To start the Celery worker, run:
# celery -A celery_worker.celery worker --loglevel=info
