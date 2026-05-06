class MinIOClient:
    def upload_text(self, bucket: str, object_key: str, content: str, content_type: str) -> dict:
        return {"bucket_name": bucket, "object_key": object_key, "file_url": f"minio://{bucket}/{object_key}", "file_size": len(content.encode("utf-8"))}
