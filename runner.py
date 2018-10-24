# -*- coding: utf-8 -*-

import sys
sys.path.append('./src/')

import BaseSnooper
from bs4 import BeautifulSoup
import re
snooper = BaseSnooper.LJSnooper("http://sh.lianjia.com")

# web = snooper.get_web_data()

# soup = BeautifulSoup(web)

# all_tags = soup.findAll(name='a', attrs={'href':re.compile("^https?://")})

# for tag in all_tags:
#    print(tag['href'])

# for i, li in enumerate(html.select('li')):
#    print(i, li.text)


# if not wb = snooper.get_web_data():
#     print("Failed to get web_data")


# if not urls = snooper.get_all_url(wb, ".*lianjia\.com"):
#     print("Failed to get all urls")

# if not snooper.process_urls():
#     print("Failed to process urls")


#snooper.tester()
snooper.run()
