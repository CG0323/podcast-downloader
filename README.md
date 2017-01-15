# podcast_downloader
A python web crawler for automatically downloading archive podcasts from Authentique Francais

====
##Table of Content
* [Background](#background)
* [Implementation](#implementation)
    * [Retrieve menu page](#retrieve-menu-page)
    * [Process detail page](#process-detail-page)
    * [Remember processed pages](#remember-processed-pages)
##Background
-----
Puisque je déménage bientôt à Montréal, c'est le temps de pratiquer beaucoup Le français.Tout d'abord, grâce à Johan, son [Français Authentique](https://www.francaisauthentique.com) est vraiment une excellente source pour améliorer le français oral.  
After follow his free course and pack1 courses, I decided to download all his podcast mp3 & pdf, then listen to them every day. As he suggests: 'Ecouter et Repeter'. All his podcast can be found on the [Archive Page](https://www.francaisauthentique.com/archive/).
If I manually download those files, I have to go into each podcast page:
![download-page](img/download-page.png)
And find the downloading link then download both the mp3 and pdf files.
This is a boring job, so I decided to use the 'to be wasted time' to practice my coding skill...

##Implementation
-----
###Retrieve menu page  
-----
First thing is to retrieve the menug page.  
```python
pip install urllib
```
```python
import urllib
response = urllib.urlopen('https://www.francaisauthentique.com/archive')
html = response.read()
```
Succeed, this page is very friendly to scrawlers :) Analyze the html, found that my interest part is as below:
```html
<h3>janvier 2017</h3>
<ul>
<li><span>13 janvier - </span> <span><a href="https://www.francaisauthentique.com/conseil-apprendre-francais-de-facon-plus-efficace/">Un conseil pour apprendre le français de façon plus efficace</a></span></li>
<li><span>11 janvier - </span> <span><a href="https://www.francaisauthentique.com/ce-se-ou-ceux/">Ce, se ou ceux ?</a></span></li>
<li><span>9 janvier - </span> <span><a href="https://www.francaisauthentique.com/invention-francaise-velo/">Une invention française : le vélo</a></span></li>
...
...
...
```
We want to get all the url into a list for further processing (each url link to a detail page of podcast, which contains the final download link), so we use 
`BeautifulSoup` to process the raw html and extract the urls, I put every thing till now into a [menu_analyzer.py](./menu_analyzer.py) module.
```python
import urllib
from bs4 import BeautifulSoup

def get_podcast_urls():
    """ Get the archive menu page, parse the html and return the list of podcast urls"""
    response = urllib.urlopen('https://www.francaisauthentique.com/archive/')
    response.close()
    html = response.read()
    soup = BeautifulSoup(html, 'html5lib')
    link_nodes = soup.select("li > span > a") #use css selector to locate our target element
    urls = [node["href"] for node in link_nodes] #use list comprehension to get all urls
    return urls
```
###Process detail page  
-----
We've got all the urls of podcast pages, now it is the time to process each page and get the mp3 and pdf files downloaded!  
Given an url, we can find the file links and download them in this way: 
```python
def download_podcast(url):
    r = urllib.urlopen(url)
    h = r.read()
    r.close()
    s = BeautifulSoup(h,'html5lib')
    links = s.find_all("a", target="_blank")
    for link in links:
        if ".mp3" in link["href"] or ".pdf" in link["href"]:
            file_name = link["href"].split('/')[-1]
            print "download: " + file_name
            urllib.urlretrieve(link["href"],file_name)
            print "finished: " + file_name
```
Loop the url list we get from menu_analyzer:
```python
urls = get_podcast_urls()
for url in urls:
    download_podcast(url)
```
At this point, this small tool already works, but due to the poor network connection here in my hometown... timeout occurs occasionally.  

###Remember processed pages 
---------
First we want to handle the exception, morevoer, We definetely don't want the program to start over again and download from the beginning, 
so it is necessary to remember the urls we aleady processed.
Since this is a very small program, we just simply use a file to keep the history list:
```python
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
```
Voilà, have a cup of coffee (or 2 cups maybe~), here we get it:
![result](img/result.png)
