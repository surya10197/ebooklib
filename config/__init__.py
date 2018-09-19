import boto3

from sqlalchemy.sql import text
from sqlalchemy import create_engine

from .fetch_config import *


# S3 Object Creation
s3 = boto3.resource('s3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key= AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME)


# PSQL Object creation
conn = create_engine(POSTGRES_CONN_LINK, encoding='utf8',
    convert_unicode=True, client_encoding='utf8').connect()


jzip_bucket = s3.Bucket(TARGET_BUCKET)

licence = s3.Bucket(LICENCE_BUCKET)

epub_source_bucket = s3.Bucket(EPUB_SOURCE_BUCKET)

preview_bucket = s3.Bucket(BOOK_PREVIEW_BUCKET)
