import config
import datetime
import uuid

from sqlalchemy.sql import text
import pymongo
from ebooklib import epub
from epub_logger import logger
from pymongo import MongoClient


client = MongoClient('mongodb://juggernaut-admin:d8b5d5b6-e2d0-410b-8f1e-396cea5a9c0c@13.127.239.3:35535')
db = client['cms']

# set metadata
def get_meta_data(ebook, book_id, new_book_id):
    logger.info('Getting metadata for book:%s', book_id)
    collection = db['book_details']
    query = {'book_id': book_id}
    books = collection.find(query).sort('version_id', pymongo.DESCENDING).limit(1)

    book = books[0]
    book_title = book['book_title']
    ebook.set_title(book_title)
    ebook.set_language('en')
    get_author(ebook=ebook, book_id=book_id, new_book_id=new_book_id)
    offline_download_url = book['offline_download_url']
    teaser = book['teaser']
    synopsis = book['synopsis']
    page_count = book['page_count']
    book_size = book['book_size']
    release_date = book['release_date']
    cover_image_data = book['cover_image_data']
    # cover_image_id = book['cover_image_id']
    version_id = book['version_id']
    status = book['status']
    metadata = book['metadata']
    is_free_read = book['is_free_read'] # make is false
    author = book['author']
    book_type = book['book_type']
    chapter_list = book['chapter_list']
    chapter_segment_count = book['chapter_segment_count']
    preview = book['preview']
    chapter_num = 0
    for chapter_id in chapter_list:
        content = ''
        collection = db['chapters']
        # print 'chapter_id', chapter_id
        query = {'chapter_id': chapter_id}
        chapters = collection.find(query)
        # print 'chapters', chapters[0]
        chapter_name = chapters[0]['chapter_name']
        segment_data = chapters[0]['segment_data']
        for segment_id in segment_data:
            collection = db['segments']
            # print 'segment_id:', segment_id
            query = {'segment_id': segment_id}
            segments = collection.find(query)
            for segment in segments:
                content += segment['content']
        # print content
        chapter_num += 1
        add_chapter(ebook=ebook, book_id=book_id, new_book_id=new_book_id, chapter_name=chapter_name, content=content, chapter_num=chapter_num)

def get_author(ebook, book_id, new_book_id):
    logger.info('Getting author data for book: %s', book_id)
    author_name = 'Surya Kant Verma'
    ebook.add_author(author_name)
    # return author_name

def add_chapter(ebook, book_id, new_book_id, chapter_name, content, chapter_num):
    logger.info('Adding chapters for book:%s', book_id)
    file_name = 'chap_' + str(chapter_num) +'.xhtml'
    chapter = epub.EpubHtml(title=chapter_name, file_name=file_name, lang='hr')
    chapter.content = content
    ebook.add_item(chapter)
    set_toc(ebook=ebook, book_id=book_id, new_book_id=new_book_id, chapter=chapter, file_name=file_name, chapter_name=chapter_name)
    set_spine(ebook=ebook, book_id=book_id, new_book_id=new_book_id, chapter=chapter)

def set_toc(ebook, book_id, new_book_id, chapter, file_name, chapter_name):
    logger.info('Setting toc for book:%s', book_id)
    ebook.toc += (epub.Link(file_name, chapter_name,),
             (
                epub.Section(chapter_name),
                (chapter,)
             )
            )

def add_ncx_and_nav(ebook, book_id, new_book_id):
    logger.info('Adding ncx and nav for book:%s', book_id)
    ebook.add_item(epub.EpubNcx())
    ebook.add_item(epub.EpubNav())
    
def define_css(ebook, book_id, new_book_id):
    logger.info('Defining css for book:%s', book_id)
    style = 'BODY {color: white;}'
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    return nav_css

def add_css(ebook, book_id, new_book_id):
    nav_css = define_css(ebook=ebook, book_id=book_id, new_book_id=new_book_id)
    ebook.add_item(nav_css)

def set_spine(ebook, book_id, new_book_id, chapter):
    logger.info('Settign spine for book:%s', book_id)
    ebook.spine = ['nav', chapter]

def upload_to_s3(book):
    logger.info('uploading %s', epub)

    logger.info('uploaded successfuly')


def convert_to_epub(ebook, book_id, new_book_id):
    logger.info('Epub conversion started')
    ebook.set_identifier(new_book_id)
    get_meta_data(ebook=ebook, book_id=book_id, new_book_id=new_book_id)
    add_ncx_and_nav(ebook=ebook, book_id=book_id, new_book_id=new_book_id)
    add_css(ebook=ebook, book_id=book_id, new_book_id=new_book_id)
    epub_name = new_book_id + '.epub'
    epub.write_epub(epub_name, ebook, {})

    # upload_to_s3(epub_name)
    # return book_id


def get_book_mapping():
    book_mappings = config.conn.execute(text("select book_id, new_book_id from book_mappings"))
    for book_mapping in book_mappings:
        ebook = epub.EpubBook()
        # print book_mapping[0], book_mapping[1]
        convert_to_epub(ebook=ebook, book_id=str(book_mapping[0]), new_book_id=str(book_mapping[1]))
        break
        
def create_book_mapping():
    logger.info('Creating book_mappings...')
    now = datetime.datetime.now()
    status = 'published'
    book_type = 'ONE-SHOT'
    try:
        books = config.conn.execute(text("select book_id from books where DATA_src=1 and status=:status and book_type=:book_type"),
                status=status, book_type=book_type)
        for book in books:
            book_id=book[0]
            result = config.conn.execute(text("select 1 from book_mappings where book_id=:book_id"),
                book_id=book_id)
            if not result.fetchone():
                new_book_id = str(uuid.uuid4()).replace('-', '')
                config.conn.execute(text("insert into book_mappings(book_id, new_book_id) values(:book_id, :new_book_id)"),
                    book_id=book_id, new_book_id=new_book_id)
            else:
                logger.info("book mapping_already exist for book= %s", book_id)
    except Exception as e:
        print e
        logger.info(e)

# create_book_mapping()
get_book_mapping()
