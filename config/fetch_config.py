import os
import json


parent_dir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(parent_dir, '.env.json')) as env_file:
    env_variables = json.load(env_file)


# PSQL DB Constants
POSTGRES_CONN_LINK = env_variables['POSTGRES_CONN_LINK']

# File Block Size
BLOCK_SIZE = int(env_variables['BLOCK_SIZE'])

# Preview Quantity Allowed
ALLOWED_PREVIEW_QUANTITY = float(env_variables['ALLOWED_PREVIEW_QUANTITY'])

# S3 Credentials
AWS_ACCESS_KEY = env_variables['AWS_ACCESS_KEY']
AWS_SECRET_ACCESS_KEY = env_variables['AWS_SECRET_ACCESS_KEY']
AWS_REGION_NAME = env_variables['AWS_REGION_NAME']

# Book Cover Constants
BOOK_COVER_CDN_PREFIX = env_variables['BOOK_COVER_CDN_PREFIX']
BOOK_COVER_BUCKET = env_variables['BOOK_COVER_BUCKET']
BOOK_COVER_DIR = env_variables['BOOK_COVER_DIRECTORY']

# Book|Epub Constatns
EPUB_SOURCE_BUCKET = env_variables['EPUB_SOURCE_BUCKET']
EPUB_SOURCE_DIR = env_variables['EPUB_SOURCE_DIRECTORY']

TARGET_PREFIX = env_variables['TARGET_PREFIX']


# File contaning file-paths of XML
SOURCE_FILE = env_variables['BIG_XML_DIR_PATH'] + env_variables['BIG_XML_FILE_NAME']

# Mode to use `SourceFile`
MODE = env_variables['MODE']

# Preview Constants
BOOK_PREVIEW_BUCKET = env_variables['BOOK_PREVIEW_BUCKET']
BOOK_PREVIEW_DIR = env_variables['BOOK_PRVIEW_DIRECTORY']
BOOK_PREVIEW_CDN_PREFIX = env_variables['BOOK_PREVIEW_CDN_PREFIX']

JUG_SIGNING_KEY_FORMAT = env_variables['JUG_SIGNING_KEY_FORMAT']

# Target Constants
TARGET_BUCKET = env_variables['TARGET_BUCKET']
TARGET_CDN = env_variables['TARGET_CDN']

# Licence File Constants
LICENCE_BUCKET = env_variables['LICENCE_BUCKET']
LICENCE_DIR = env_variables['LICENCE_DIRECTORY']

# Code Constants
PUBLISHER_BLOCKS = env_variables['PUBLISHER_BLOCKS']
CURRENCY_TYPE_DICT = env_variables['CURRENCY_TYPE_DICT']
TAX_TYPE_DICT = env_variables['TAX_TYPE_DICT']

DOC_REPO_URL = env_variables['DOC_REPO_URL']
BASE_IMAGE_URL = env_variables['BASE_IMAGE_URL']
EPUB_DIR = env_variables['EPUB_DIR']
COVER_IMAGE_DIR = env_variables['COVER_IMAGE_DIR']
INLINE_IMAGE_DIR = env_variables['INLINE_IMAGE_DIR']
USER_NAME = env_variables['USER_NAME']
HOST = env_variables['HOST']
PASSWORD = env_variables['PASSWORD']
PORT = env_variables['PORT']
DB_NAME = env_variables['DB_NAME']
SSL_MODE = env_variables['SSL_MODE']
MONGO_CONN_LINK = env_variables['MONGO_CONN_LINK']
