import datetime
import os
import configparser
import progressbar
import string
import codecs
import json

from instapaper import Instapaper

# Init instapaper with key, secret, login and password
def init():
    # Read credentials from Credentials.ini file
    configParser = configparser.RawConfigParser()
    configParser.read('Credentials.ini')

    key = configParser.get('Instapaper', 'INSTAPAPER_KEY')
    secret = configParser.get('Instapaper', 'INSTAPAPER_SECRET')
    login = configParser.get('Login', 'INSTAPAPER_LOGIN')
    password = configParser.get('Login', 'INSTAPAPER_PASSWORD')

    # Create instance of Instapaper using the OAth credentials
    instapaper = Instapaper(key, secret)

    # Login with user and password
    instapaper.login(login, password)

    return instapaper

def process_folder(folderid, existing):

    # Get bookmarks from archive for each of the folders
    bookmarks = instapaper.bookmarks(folder=folderid, have=existing, limit=500)

    # process all bookmarks
    process_bookmarks(bookmarks)

def check_saved_state():
    # If there is no file in with bookmark hashes then create it
    file_exists = os.path.isfile("saved_state.txt")

    if file_exists:
        print("Last State Exists")
        # read file contents to existing
        existing=get_list_of_existing_highlights()
        return existing

def process_saved_state(foldername):
    bookmarks = instapaper.bookmarks(folder=foldername, have="", limit=500)
    for bookmark in bookmarks:
        fp = open("../saved_state.txt", "a+")
        fp.write(str(bookmark.bookmark_id) + ":" + bookmark.hash + ",")


def get_list_of_existing_highlights():
    # Get all .md files in current directory
    text_file = open("saved_state.txt", "r")
    existing = text_file.readlines()
    return existing

def change_to_highlights_folder():
    # If there is no folder in the system with highlights then create it
    if not os.path.exists('highlights'):
        os.makedirs('highlights')

    # Change to the folder
    os.chdir('highlights')

# Process list of bookmarks
def process_bookmarks(bookmarks):
    progress = progressbar.ProgressBar(maxval=len(bookmarks))
    i = 1
    progress.start()
    for bookmark in bookmarks:
        process_bookmark(bookmark)
        progress.update(i)
        i = i + 1
    progress.finish()

def get_filename_from_title(title):
    """Generate simpler file name from title

    Arguments:
        title {string} -- Simplified title to be used as the markdown filename
    """
    printable = set(string.ascii_letters)
    printable.add(' ')
    return ''.join(filter(lambda x : x in printable, title)).strip().replace(' ', '_') + '.md'

# Process the highlights of one bookmark
def process_bookmark(bookmark):

    # Get the highlights
    highlights = bookmark.get_highlights()

    #print(highlights) if there is any highlight
    if len(highlights) > 0:
        process_document(bookmark, highlights)

def process_document(bookmark, highlights):
    """Takes a document and generates the equivalent markdown file

    Arguments:
        document {dictionary} -- Dictionary with title, url and list of highlights
    """
    output_path = get_filename_from_title(bookmark.title)

    #parse highlights as JSON
    highlights_json=json.loads(highlights)

    # count number of highlights with a given bookmark id
    highlight_count = len(highlights_json)

    if(highlight_count>0):
        with codecs.open(output_path, 'w', 'utf-8') as f:
            f.write('# ' + bookmark.title + '\n')
            f.write('\n')
            f.write('[Source](' + bookmark.url + ')' + '\n')
            f.write('\n')
            f.write(repr(highlight_count) + ' highlights' +'\n')
            f.write('\n')
            f.write('---' + '\n')
            f.write('\n')

            index=0;
            while index < highlight_count:
                f.write('* '+ highlights_json[index]['text'])
                if highlights_json[index]['note']!= None:
                    f.write("[^" + str(highlights_json[index]['highlight_id']) + "]")
                    f.write('\n\n')
                    f.write("[^" + str(highlights_json[index]['highlight_id']) + "]: " + str(highlights_json[index]['note']) + '\n')

                f.write('\n\n')
                index=index+1;

# ----------------------------------
# Init Instapaper
instapaper = init()

# Get existing highlights
existing=check_saved_state()

# Change to highlights folder
change_to_highlights_folder()

# Get list of folders
folders = instapaper.folders()
folders = [{"folder_id": "archive"}, {"folder_id": "starred"}] + folders

# Process bookmarks for each folder
for folder in folders:
    if (folder['folder_id']=="archive" or folder['folder_id']=="starred"):
        print("Processing Folder: " + folder['folder_id'])
    else:
        print("Processing Folder: " + folder['title'])

    process_folder(folder['folder_id'], existing)


# create new file and add hash of all bookmarks
if os.path.exists("saved_state.txt"):
  os.remove("saved_state.txt")

progress = progressbar.ProgressBar(maxval=len(folders))
progress.start()
print("Writing Last Saved States:")
for folder in folders:
    i = 1
    process_saved_state(folder['folder_id'])
    progress.update(i)
    i = i + 1
progress.finish()
