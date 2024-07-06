# Image Processing System

This project is an image processing system built using FastAPI, SQLAlchemy, Celery, and Redis. The system processes images uploaded via a CSV file, compresses them, and updates their status in the database.

## Features

- Upload CSV files containing image URLs for processing.
- Compress and store processed images.
- Check the status of image processing requests.
- Use Celery for asynchronous image processing tasks.

## Requirements

- Python 3.8+
- FastAPI
- SQLAlchemy
- Celery
- Redis
- Requests
- Pydantic
- Uvicorn
- Other dependencies specified in `requirements.txt`

## Installation

1. Clone the repository:

```sh
git clone https://github.com/piyushkashyap07/Image_processing_system.git
cd image-processing-system
