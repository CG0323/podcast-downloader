import urllib
from bs4 import BeautifulSoup
from menu_analyzer import get_podcast_urls
import pickle
import os.path

def download_podcast(url):
    """Given an url of podcast detail page, retrieve the page, parse the content and then download mp3 and pdf files"""
    history = []
    if os.path.exists('history'):
        with open('history', 'rb') as fp:
            history = pickle.load(fp)
    if url in history:
        return
    try:
        response = urllib.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html5lib')
        links = soup.find_all("a", target="_blank")
        for link in links:
            if ".mp3" in link["href"] or ".pdf" in link["href"]:
                file_name = link["href"].split('/')[-1]
                print "download: " + file_name
                urllib.urlretrieve(link["href"], file_name)
                print "finished: " + file_name
                history.append(url)
                with open('history', 'wb') as fp:
                    pickle.dump(history, fp)
    finally:
        if response:
            response.close()

def download_podcasts():
    """Download all podcasts from Francais Authentique Archive"""
    url_list = get_podcast_urls()
    for url in url_list:
        download_podcast(url)

if __name__ == '__main__':
    download_podcasts()



