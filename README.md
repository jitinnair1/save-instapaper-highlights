# save-instapaper-highlights

A simple application to save notes and highlights from Instapaper.

The downloader checks for highlights and notes from bookmarks in all folders created by the user along with the standard `archive` and `starred` folders.

It then creates a folder called `highlights`. For each bookmark, it creates a Markdown file in `highlights` including the title of the bookmark, url reference and all the highlights and notes.

Lastly, it creates a `saved_state.txt` file with `hash` values for each bookmark which is computed from its URL, title, description, and reading progress. Bookmarks are not processed if the hashes haven't changed. So the application will download only incremental changes on subsequent runs.

## Installation

```
pip install -r requirements.txt
```

## Usage

1. Get a KEY and SECRET OAuth from [Instapaper](https://www.instapaper.com/main/request_oauth_consumer_token)
2. Modify the file Credentials.ini with your KEY, SECRET, LOGIN and PASSWORD
3. Call the app `python downloader.py`

## Based on

 This app makes use of [Instapaper API Python wrapper](https://github.com/rsgalloway/instapaper) and is based on [highlightsdownloader](https://github.com/alberto-old/highlightsdownloader)
 
<a href="https://www.buymeacoffee.com/jitinnair" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>
