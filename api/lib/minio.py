
from fastapi import HTTPException, status, UploadFile, File

import time
import hashlib
import shutil
from minio import Minio
from datetime import timedelta

class MinioClient:
    def __init__(self, endpoint: str, access_key: str, secret_key: str, bucket_name: str):
        self.client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=True
        )
        self.bucket_name = bucket_name

    def create_bucket(self):
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)

    def upload_file(self, file: UploadFile, file_size):
        try:        
            result = self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=file.filename,
                data=file.file,
                length=file_size,
            )
            return result.version_id
        except Exception as e:
            self._exception(f"Error while trying to upload file. Exception: {e}")

    def download_file(self, source: str, destination: str):
        try:
            self.client.fget_object(self.bucket_name, source, destination)
        except Exception as e:
            self._exception(f"Error while trying to download file. Exception: {e}")

    def get_url(self, bucket_name:str, object_name:str, limit:int=2):
        try:
            url = self.client.get_presigned_url(
                "GET",
                bucket_name=bucket_name,
                object_name=object_name,
                expires=timedelta(hours=limit),
            )
            return url
        except Exception as e:
            self._exception(f"Error while trying to Get URL. Exception: {e}")

    def _exception(self, detail: str):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )
