from ebooklib import epub
import ebooklib

book = epub.read_epub('epub/A-Room-with-a-View-morrison.epub')


for image in book.get_items_of_type(ebooklib.ITEM_IMAGE):
    print "Images : " + str(image)

for image in book.get_items_of_type(ebooklib.ITEM_STYLE):
    print "Style : " + str(image)

for image in book.get_items_of_type(ebooklib.ITEM_SCRIPT):
    print "Script : " + str(image)

for image in book.get_items_of_type(ebooklib.ITEM_NAVIGATION):
    print "Navigation : " + str(image)

for image in book.get_items_of_type(ebooklib.ITEM_VECTOR):
    print "Vector : " + str(image)

for image in book.get_items_of_type(ebooklib.ITEM_FONT):
    print "Font : " + str(image)
    print type(image)

for image in book.get_items_of_type(ebooklib.ITEM_VIDEO):
    print "Video : " + str(image)

for image in book.get_items_of_type(ebooklib.ITEM_AUDIO):
    print "Audio : " + str(image)

for doc in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
    ##print image.__dict__.viewkeys()

    for key, value in doc.__dict__.iteritems():
        print(key, value)
        if key == 'content':

            print("key is = "+ key)
            doc.__dict__[key] = "Surya Kant Verma"
        print "++++++++++++++++++++++++++++"


epub.write_epub('test.epub', book, {})

    #print image

#print book.get_template('chapter-020-the-end-of-the-middle-ages.html')
#print book.get_item_with_href('EPUB/document.xhtml')

#print book.get_item_with_id()
#f = open("chapter-002:OEBPS/chapter-002-in-santa-croce-with-no-baedeker.html","w")
#print f
