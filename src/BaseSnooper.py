# -*- coding: utf-8 -*-


import requests
import contextlib
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

SUCCESS = True
FAILURE = False

class BaseSnooper:
    
    def __init__(self, base_url):
        self.base_url = base_url
        self.sites = set()
        self.visited = set()
        self.rule = ''

    def get_web_data(self, url):
        try:
            with contextlib.closing(requests.get(url, stream=True)) as resp:
                if self.is_good_response(resp):
                    web_data = resp.content
                    return web_data
                else:
                    return FAILURE

        except requests.RequestException as e:
            print('Error during requests to {0} : {1}'.format(url, str(e)))
            return FAILURE
    
    def is_good_response(self, resp):
        content_type = resp.headers['Content-Type'].lower()
        return(resp.status_code == 200
               and content_type is not None
               and content_type.find('html') > -1)

    def get_local_urls(self, web_data, rule):
        urls = []
        soup = BeautifulSoup(web_data, 'lxml')
        rule = "^https?://" + rule
        tags = soup.findAll(name='a', attrs={'href':re.compile(rule)})

        for tag in tags:
            try:
                tmp = tag['href']
                urls.append(tag['href'])
            except:
                print("Maybe not the attr : href")
                continue


        print("Fetched urls: " + str(len(urls)))
        return urls

    
    #def get_local_pages(self):
    def process_urls(self, urls):
        print("Template method, just return original urls")

        processed_urls = urls
        
        return processed_urls

    def dfs(self, pages):
        if pages is set():
            return
        self.sites = set.union(self.sites, pages)
        for page in pages:
            if page not in self.visited:
                print("Visiting", page)
                self.visited.add(page)
                url = page
                web_data = self.get_web_data(page)
                pages = self.get_local_urls(web_data, self.rule)
                processed_pages = self.process_urls(pages)
                self.dfs(processed_pages)

    def run(self):
        web_data = self.get_web_data(self.base_url)
        pages = self.get_local_urls(web_data, self.rule)
        self.dfs(pages)
        for site in self.sites:
            print(site)
        
    
    
class LJSnooper(BaseSnooper):

    def __init__(self, base_url):
        BaseSnooper.__init__(self, base_url)

        self.rule = ".*sh\.lianjia\.com"
        
    def process_urls(self, urls):
        processed_urls = set()
        for url in urls:
            o = urlparse(url)

            if self.is_relative_path(o):
                fixed_url = self.process_relative_path(o)
            else:
                fixed_url = o.geturl()

            if 'http' not in o[0]:
                print("Bad page: " + fixed_url.encode('acsii'))
                continue

            if self.is_correct(o):
                print("Bad page: " + fixed_url.encode('ascii'))
                continue

            if fixed_url not in processed_urls:
                #print("Add New Page: " + fixed_url)
                processed_urls.add(fixed_url)
        return processed_urls
        
    def is_correct(self, o):
        return o[0] == "" and o[1] != ""
        
    def is_relative_path(self, o):
        return o[0] == "" and o[1] == ""

    def process_relative_path(self, o):
        print("Processing relative path: " + o.geturl() + "...")

        url_obj = urlparse(self.base_url)
        fixed_url = url_obj[0] + "://" + url_obj[1] + url_obj[2] + o.geturl()
        fixed_url = fixed_url[:8] + fixed_url[8:].replace('//', '/')
        new_o = urlparse(fixed_url)

        if '../' in new_o[2]:
            paths = o[2].split('/')
            for i in range(len(paths)):
                if paths[i] == '..':
                    paths[i] = ''
                    if paths[i - 1]:
                        paths[i - 1] = ''
            tmp_path = ''
            for path in paths:
                if path == '':
                    continue
                tmp_path = tmp_path + '/' + path
            fixed_url = fixed_url.replace(new_o[2], tmp_path)
        print("Processed url: " + fixed_url)
        return fixed_url
    
    def tester(self):
        o = urlparse("/abc/bca")
        print(o)
        if (self.is_relative_path(o)):
            print("YES RP")
        if self.is_correct(o):
            print("YES CO")
        self.process_relative_path(o)
