import requests
import contextlib
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse


SUCCESS = True
FAILURE = False

class NovelCatcher:
    def __init__(self, base_url):
        self. base_url = base_url
        self.web_data = None

    def get_web_data(self, url):
        try:
            with contextlib.closing(requests.get(url, stream=True)) as resp:
                if self.is_good_response(resp):
                    self.web_data = resp.content
                    return SUCCESS
                else:
                    return FAILURE
        except requests.RequestException as e:
            print('Error during requests to {0} : {1}'.format(url, str(e)))
            return FAILURE


    def is_good_reponse(self, resp):
        content_type = resp.headers['Content-Type'].lower()
        return(resp.status_code == 200
               and contxt_type is not None
               and contxt_type.find('html') > -1)

    def get_chapter_urls(self, rule):

        urls = []
        
        soup = BeautifulSoup(self.web_data, 'lxml')

        tags = soup.findAll(name='a', attrs={'href':re.compile(rule)})

        for tag in tags:
            try:
                tmp = tag['href']
                urls.append(tag['href'])
            except:
                print('Maybe not the attr: href')
                continue

        print("Fetched urls: " + str(len(urls)))
        return urls



catcher = NovelCatcher("https://www.qq717.com/html/40/40198/")
if not catcher.get_web_data():
    print("cannot get web data")
    exit(1)

urls = catcher.get_chapter_urls("/html/40/40198/")
