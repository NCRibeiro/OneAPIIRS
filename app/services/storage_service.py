from core.settings import settings
from typing import Any


def upload_file(file_path: str, destination: str) -> Any:
    bucket = settings._raw_bucket
    blob = bucket.blob(destination)
    blob.upload_from_filename(file_path)
    return blob.public_url
