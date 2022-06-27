import aioboto3
from pydantic import BaseSettings
from time import time
from fastapi import UploadFile
import asyncio
import os

class S3Bucket(BaseSettings):
    AWS_S3_BUCKET_NAME_STATIC: str = "random_bucket_name"
    AWS_S3_PUBLIC_URL: str = "https://randome_s3_url"


class HarmonyS3:
    def __init__(self, bucket_name, public_url, service_name):
        self.bucket_name = bucket_name
        self.public_url = public_url
        self.service_name = service_name

    def upload_location(self, dir_name, filename):
        extension = filename.split(".")[-1]
        name = filename.split(".")[0]
        return f"{self.service_name}/{dir_name}/{int(time())}_{name}.{extension}"

    async def upload_files(self, file_objs: list[UploadFile], dir_name):
        session = aioboto3.Session()
        async with session.client("s3") as s3:
            tasks = {}
            for order, file_obj in enumerate(file_objs):
                fname, extension = os.path.splitext(file_obj.filename)
                filename = fname + str(order) + extension
                filepath = self.upload_location(dir_name, filename=filename)
                task = asyncio.create_task(s3.upload_fileobj(file_obj, self.bucket_name, filepath), name=filename)
                tasks[filepath] = task

            await asyncio.gather(*tasks.values())
            for task in tasks:
                yield task

    @staticmethod
    def upload_to_bucket(file_objs, dir_name):
        bucket_info: S3Bucket = S3Bucket()
        s3 = HarmonyS3(
            bucket_name=bucket_info.AWS_S3_BUCKET_NAME_STATIC,
            public_url=bucket_info.AWS_S3_PUBLIC_URL,
            service_name="random_service_name",
        )
        return s3.upload_files(file_objs, dir_name)  # Coroutine
