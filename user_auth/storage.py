
from storages.backends.s3boto3 import S3Boto3Storage


# S3 Storage Conf

class S3ImageStorage(S3Boto3Storage):
    location = 'media/images'  
    file_overwrite = False 