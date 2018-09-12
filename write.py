import config
import datetime
import uuid

from sqlalchemy.sql import text
import pymongo
from ebooklib import epub
from epub_logger import logger
from pymongo import MongoClient
from slugify import slugify
# from encryption import AESEncryption, generate_encrypted_file

# aes = AESEncryption()
client = MongoClient('mongodb://juggernaut-admin:d8b5d5b6-e2d0-410b-8f1e-396cea5a9c0c@13.127.239.3:35535')
db = client['cms']
syno = list()
cover = list()
epub_dir = '/media/storage2/data/epub/'
# jzip = '/media/storage2/data/jzip/'
# lic = '/media/storage2/data/lic/'
# html = '/media/storage2/data/html/'

issue_with_books = list()
# def get_slug(book_id, title, suffix):
#     try:
#         slug = slugify(title)
#     except Exception:
#         slug = "-".join(title.strip().lower().split(' '))
#     if suffix != 0:
#         slug = slug + '-' + str(suffix)
#     result = config.conn.execute(text("select 1 from books where permalink_slug=:slug"),
#             slug=slug)
#     if not result.fetchone():
#         return slug
#     else:
#         suffix = suffix + 1
#         return get_slug(book_id=book_id, title=title, suffix=suffix)


# def generate_preview(book_id, new_book_id, preview):
#     logger.info('Generating Preview for book:%s', new_book_id)
#     for segment_preview in preview:
#         segment_id = segment_preview['segment_id']
#         collection = db['segments']
#         query = {'segment_id': segment_id}
#         segments = collection.find(query)
#         content = ''
#         for segment in segments:
#             # print segment['content']
#             content += segment['content']
#
#         content = content.encode('utf-8')
#         file_name = html + new_book_id + '.html'
#         file = open(file_name, "w")
#         file.write("<html>" + content + "</html>")
#         file.close()

def get_meta_data(ebook, book_id, new_book_id):
    now = datetime.datetime.now()
    logger.info('Getting metadata for book book_id: %s and new_book_id:%s', book_id, new_book_id)
    collection = db['book_details']
    query = {'book_id': book_id}
    books = collection.find(query).sort('version_id', pymongo.DESCENDING).limit(1)
    book = books[0]
    book_title = book.get('book_title', '')
    ebook.set_title(book_title)
    # check allowed language
    ebook.set_language('en')
    get_set_author(ebook=ebook, book_id=book_id, new_book_id=new_book_id)
    teaser = book.get('teaser', '')
    synopsis = book.get('synopsis', None)
    page_count = book.get('page_count', None)
    book_size = book.get('book_size', None)
    cover_image_data = book.get('cover_image_data')
    print 'cover_image_data : ', cover_image_data
    # cover_image_data1 = config.BOOK_COVER_CDN_PREFIX + new_book_id + '.jpg',
    # preview_url = config.BOOK_PREVIEW_CDN_PREFIX + new_book_id + '.html',
    cover_image_id = book.get('cover_image_id')
    if cover_image_id:
        print 'cover_found'
    else:
        cover.append(book_id)
        print 'cover_not'
    # print 'teaser', teaser
    if synopsis:
        print 'synopsis:', 'Found'
    else:
        syno.append(book_id)
        print 'synopsis:', 'Not Found'
    chapter_list = book.get('chapter_list')
    # print 'chapter_list', chapter_list
    chapter_num = 0
    # try:
    #     result = config.conn.execute(text("select 1 from books where book_id=:new_book_id"),
    #                                  new_book_id=new_book_id)
    #     if not result.fetchone():
    #         config.conn.execute(text("insert into books(book_id, book_title, created_at, updated_at, is_internal, release_date, status, show_as_coming_soon, permalink_slug, data_src, content_src, language, book_type, is_free_read, is_all_access)"
    #                                  " select :new_book_id, book_title, :created_at, :updated_at, is_internal, release_date, 'new', show_as_coming_soon, concate(permalink_slug, '1'), :data_src, content_src, language, book_type, is_free_read, is_all_access"
    #                                  " from books where book_id=:book_id"), book_id=book_id, new_book_id=new_book_id, created_at=now, updated_at=now, data_src=3)
    #     else:
    #         print 'Book already created :%s', new_book_id
    #         logger.info('Book already created :%s', new_book_id)
    # except Exception as e:
    #     print 'Entry already created old book :%s new book_id:%s', book_id, new_book_id
    #     logger.info('Entry already created old book :%s new book_id:%s', book_id, new_book_id)
    #
    # try:
    #     result = config.conn.execute(text("select 1 from book_meta where book_id=:new_book_id"),
    #                                  new_book_id=new_book_id)
    #     if not result.fetchone():
    #         config.conn.execute(text("insert into book_meta(version_id, cover_image_data, cover_image_id, teaser, synopsis, page_count, book_size, book_id, ask_the_author, show_chapter_no, is_subscribable)"
    #                                  " values (1, :cover_image_data, :cover_image_id, :teaser, :synopsis, :page_count, :book_size, :new_book_id, :ask_the_author, :show_chapter_no, :is_subscribable)")
    #                             , cover_image_data=cover_image_data, cover_image_id=cover_image_id, teaser=teaser, synopsis=synopsis, page_count=page_count, book_size=book_size, new_book_id=new_book_id,
    #                             ask_the_author=False, show_chapter_no=False, is_subscribable=True)
    #
    #     else:
    #         print 'Meta info already present for book:%s', new_book_id
    #         logger.info('Meta info already present for book:%s', new_book_id)
    #
    # except Exception as e:
    #     print 'Entry already created for book_meta old book :%s new book_id:%s', book_id, new_book_id
    #     logger.info('Entry already created for book_meta old book :%s new book_id:%s', book_id, new_book_id)
    #
    # try:
    #     result = config.conn.execute(text("select 1 from author_books where book_id=:new_book_id"),
    #                                  new_book_id=new_book_id)
    #     if not result.fetchone():
    #         config.conn.execute(text(
    #             "insert into author_books(created_at, updated_at, author_id, book_id)"
    #             " select created_at, updated_at, author_id, :new_book_id"
    #             " from author_books where book_id=:book_id"), book_id=book_id, new_book_id=new_book_id, created_at=now,
    #                             updated_at=now)
    #     else:
    #         print 'Author Book already created :%s', new_book_id
    #         logger.info('Author Book already created :%s', new_book_id)
    #
    # except Exception as e:
    #     print 'Entry already created for author_books old book :%s new book_id:%s', book_id, new_book_id
    #     logger.info('Entry already created for author_books old book :%s new book_id:%s', book_id, new_book_id)
    #
    # try:
    #     result = config.conn.execute(text("select 1 from book_tags where book_id=:new_book_id"),
    #                                  new_book_id=new_book_id)
    #     if not result.fetchone():
    #         config.conn.execute(text(
    #             "insert into book_tags(book_id, tag_id, created_at, updated_at)"
    #             " select :new_book_id, tag_id, created_at, updated_at"
    #             " from book_tags where book_id=:book_id"), book_id=book_id, new_book_id=new_book_id, created_at=now,
    #             updated_at=now)
    #     else:
    #         print 'Tag Book already created :%s', new_book_id
    #         logger.info('Tag Book already created :%s', new_book_id)
    #
    # except Exception as e:
    #     logger.info('Entry already created for book_tags old book :%s new book_id:%s', book_id, new_book_id)
    #
    # try:
    #     result = config.conn.execute(text("select 1 from book_publishers where book_id=:new_book_id"),
    #                                  new_book_id=new_book_id)
    #     if not result.fetchone():
    #         config.conn.execute(text(
    #             "insert into book_publishers(created_at, updated_at, book_id, publisher_id)"
    #             " select created_at, updated_at, :new_book_id, publisher_id"
    #             " from book_publishers where book_id=:book_id"), book_id=book_id, new_book_id=new_book_id, created_at=now,
    #             updated_at=now)
    #     else:
    #         logger.info('Publishers Book already created :%s', new_book_id)
    #
    # except Exception as e:
    #     logger.info('Entry already created for book_publishers old book :%s new book_id:%s', book_id, new_book_id)
    #
    # try:
    #     result = config.conn.execute(text("select 1 from book_area where book_id=:new_book_id"),
    #                                  new_book_id=new_book_id)
    #     if not result.fetchone():
    #         config.conn.execute(text(
    #             "insert into book_area(active, start_date, end_date, area_id, book_id)"
    #             " select active, start_date, end_date, area_id, :new_book_id"
    #             " from book_tags where book_id=:book_id"), book_id=book_id, new_book_id=new_book_id)
    #     else:
    #         logger.info('Area Book already created :%s', new_book_id)
    #
    # except Exception as e:
    #     logger.info('Entry already created for book_area old book :%s new book_id:%s', book_id, new_book_id)
    #
    # try:
    #     result = config.conn.execute(text("select 1 from book_prices where book_id=:new_book_id"),
    #                                  new_book_id=new_book_id)
    #     if not result.fetchone():
    #         config.conn.execute(text(
    #             "insert into book_prices(base_price, base_price_currency, created_at, updated_at, book_id, inclusive_of_taxes, country_codes)"
    #             " select base_price, base_price_currency, :created_at, :updated_at, :new_book_id, inclusive_of_taxes, country_codes"
    #             " from book_prices where book_id=:book_id"), book_id=book_id, new_book_id=new_book_id, updated_at=now, created_at=now)
    #     else:
    #         logger.info('Prices Book already created :%s', new_book_id)
    #
    # except Exception as e:
    #     logger.info('Entry already created for book_prices old book :%s new book_id:%s', book_id, new_book_id)

    for chapter_id in chapter_list:
        content = ''
        collection = db['chapters']
        query = {'chapter_id': chapter_id}
        chapters = collection.find(query)
        segment_data = chapters[0].get('segment_data')
        for segment_id in segment_data:
            collection = db['segments']
            query = {'segment_id': segment_id}
            segments = collection.find(query)
            for segment in segments:
                content += segment.get('content')
        chapter_num += 1
        chapter_name = 'Chapter ' + str(chapter_num)
        # print 'content', content.encode('ascii', 'ignore')
        add_chapter(ebook=ebook, book_id=book_id, new_book_id=new_book_id, chapter_name=chapter_name, content=content, chapter_num=chapter_num)


def get_set_author(ebook, book_id, new_book_id):
    logger.info('Getting author data for book book_id: %s and new_book_id:%s', book_id, new_book_id)
    authors = config.conn.execute(text("select name from authors where author_id in (select author_id from author_books where book_id=:book_id)"),
                                 book_id=book_id)
    author_name = ''
    for author in authors:
        # print author
        author_name += author[0]
    ebook.add_author(author_name)


def add_chapter(ebook, book_id, new_book_id, chapter_name, content, chapter_num):
    logger.info('Adding chapters for book book_id: %s and new_book_id:%s', book_id, new_book_id)
    file_name = 'chap_' + str(chapter_num) +'.xhtml'
    chapter = epub.EpubHtml(title=chapter_name, file_name=file_name, lang='hr')
    chapter.content = content
    ebook.add_item(chapter)
    set_toc(ebook=ebook, book_id=book_id, new_book_id=new_book_id, chapter=chapter, file_name=file_name, chapter_name=chapter_name)
    set_spine(ebook=ebook, book_id=book_id, new_book_id=new_book_id, chapter=chapter)


def set_toc(ebook, book_id, new_book_id, chapter, file_name, chapter_name):
    logger.info('Setting toc for book book_id: %s and new_book_id:%s', book_id, new_book_id)
    # ebook.toc += (epub.Link(file_name, chapter_name,),
    #                 (
    #                     epub.Section(chapter_name),
    #                     (chapter,)
    #                  )
    #         )

    # ebook.toc.append(epub.Link(file_name, chapter_name, 'intro'))
    ebook.toc.append(epub.Link(file_name, chapter_name, 'intro'))


def add_ncx_and_nav(ebook, book_id, new_book_id):
    logger.info('Adding ncx and nav for book book_id: %s and new_book_id:%s', book_id, new_book_id)
    ebook.add_item(epub.EpubNcx())
    ebook.add_item(epub.EpubNav())


def define_css(ebook, book_id, new_book_id):
    logger.info('Defining css for book book_id: %s and new_book_id:%s', book_id, new_book_id)
    style = 'BODY {color: white;}'
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    return nav_css


def add_css(ebook, book_id, new_book_id):
    logger.info('Adding css for book book_id: %s and new_book_id:%s', book_id, new_book_id)
    nav_css = define_css(ebook=ebook, book_id=book_id, new_book_id=new_book_id)
    ebook.add_item(nav_css)


def set_spine(ebook, book_id, new_book_id, chapter):
    logger.info('Settign spine for book book_id: %s and new_book_id:%s', book_id, new_book_id)
    ebook.spine.append(chapter)


def convert_to_epub(ebook, book_id, new_book_id):
    logger.info('Epub conversion started for book book_id: %s and new_book_id:%s', book_id, new_book_id)
    ebook.set_identifier(new_book_id)
    get_meta_data(ebook=ebook, book_id=book_id, new_book_id=new_book_id)
    add_ncx_and_nav(ebook=ebook, book_id=book_id, new_book_id=new_book_id)
    add_css(ebook=ebook, book_id=book_id, new_book_id=new_book_id)
    epub_name = epub_dir + new_book_id + '.epub'
    ebook.spine.append('nav')
    # try:
    #     epub.write_epub(epub_name, ebook, {})
    # except Exception as e:
    #     print 'Issue with old book :', book_id
    #     issue_with_books.append(book_id)
    #     logger.info('Issue with book book_id: %s and new_book_id:%s', book_id, new_book_id)


def get_book_mapping():
    logger.info('Getting books mapping...')
    book_mappings = config.conn.execute(text("select book_id, new_book_id from book_mappings"))
    for book_mapping in book_mappings:
        ebook = epub.EpubBook()
        print book_mapping[0], book_mapping[1]
        convert_to_epub(ebook=ebook, book_id=str(book_mapping[0]), new_book_id=str(book_mapping[1]))

def create_book_mapping():
    logger.info('Creating book_mappings...')
    status = 'published'
    book_type = 'ONE-SHOT'
    collection = db['book_details']
    query = [{"$match": {"status": status, "book_type": book_type}}, {"$group": {"_id": "$book_id", "version_id": {"$max":"$version_id"}}}]
    all_books = collection.aggregate(query)
    book_list = list()
    for book in all_books:
        book_list.append(book['_id'])
    book_type = 'SERIALIZED'
    collection = db['book_details']
    query = {"status": status, "book_type": book_type}
    books = collection.find(query)
    for b in books:
        child_ids = b['child_ids']
        for child_id in child_ids:
            if child_id in book_list:
                book_list.remove(child_id)

    try:
        book_type = 'ONE-SHOT'
        for book_id in book_list:
            books = config.conn.execute(text("select 1 from books where book_id=:book_id and data_src=1 and status=:status and book_type=:book_type"),
                book_id=book_id, status=status, book_type=book_type)
            if books.fetchone():
                result = config.conn.execute(text("select 1 from book_mappings where book_id=:book_id"),
                    book_id=book_id)
                if not result.fetchone():
                    new_book_id = str(uuid.uuid4()).replace('-', '')
                    config.conn.execute(text("insert into book_mappings(book_id, new_book_id) values(:book_id, :new_book_id)"),
                        book_id=book_id, new_book_id=new_book_id)
                else:
                    logger.info('book mapping_already exist book book_id: %s and new_book_id:%s', book_id, new_book_id)
            else:
                logger.info('Book not found %s', book_id)
    except Exception as e:
        logger.info(e)

create_book_mapping()
get_book_mapping()

print 'Issue with books'
print issue_with_books
print 'count', len(issue_with_books)
print 'syn not found :', len(syno)
print 'cover id not found :', (cover)

