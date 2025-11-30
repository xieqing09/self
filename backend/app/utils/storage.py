from app.core.config import settings
import io
import os
import aiofiles

class StorageClient:
    def upload_file(self, file_data: bytes, filename: str, bucket: str) -> str:
        raise NotImplementedError
    
    def get_file(self, filename: str, bucket: str):
        raise NotImplementedError

class LocalStorage(StorageClient):
    def __init__(self):
        self.base_path = settings.LOCAL_STORAGE_PATH
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
    
    def _get_bucket_path(self, bucket: str):
        path = os.path.join(self.base_path, bucket)
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def upload_file(self, file_data: bytes, filename: str, bucket: str) -> str:
        bucket_path = self._get_bucket_path(bucket)
        file_path = os.path.join(bucket_path, filename)
        
        # Sync write for simplicity or use aiofiles if purely async context needed
        # But here we are mimicking MinIO client which is usually blocking or wrapped
        with open(file_path, "wb") as f:
            f.write(file_data)
            
        return file_path

    def get_file(self, filename: str, bucket: str):
        bucket_path = self._get_bucket_path(bucket)
        file_path = os.path.join(bucket_path, filename)
        with open(file_path, "rb") as f:
            return f.read()

class MinioClient(StorageClient):
    def __init__(self):
        from minio import Minio
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        self._ensure_buckets()

    def _ensure_buckets(self):
        for bucket in [settings.MINIO_BUCKET_UPLOADS, settings.MINIO_BUCKET_MODELS]:
            if not self.client.bucket_exists(bucket):
                self.client.make_bucket(bucket)

    def upload_file(self, file_data: bytes, filename: str, bucket: str) -> str:
        file_stream = io.BytesIO(file_data)
        self.client.put_object(
            bucket,
            filename,
            file_stream,
            length=len(file_data)
        )
        return f"{bucket}/{filename}"

    def get_file(self, filename: str, bucket: str):
        return self.client.get_object(bucket, filename)

# Factory
if settings.USE_LOCAL_STORAGE:
    storage = LocalStorage()
else:
    storage = MinioClient()
