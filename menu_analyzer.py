import urllib
from bs4 import BeautifulSoup

def get_podcast_urls():
    """ Get the archive menu page, parse the html and return the list of podcast urls"""
    response = urllib.urlopen('https://www.francaisauthentique.com/archive/')
    html = response.read()
    response.close()
    soup = BeautifulSoup(html, 'html5lib')
    link_nodes = soup.select("li > span > a") #use css selector to locate our target element
    urls = [node["href"] for node in link_nodes] #use list comprehension to get all urls
    return urls

if __name__ == '__main__':
    print "\n".join(get_podcast_urls())
