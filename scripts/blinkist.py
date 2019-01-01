# -*- coding: utf-8 -*-
import json
import os
import urllib2 
import cookielib

from bs4 import BeautifulSoup
import mechanize
import urllib2

cook = cookielib.CookieJar()
req = mechanize.Browser()
req.set_cookiejar(cook)

req.open("https://www.blinkist.com/en/nc/login/")
req.select_form(nr=0)


print('Hello! 👋')
req.form['login[email]'] = os.environ['BLINKIST_EMAIL']
req.form['login[password]'] = os.environ['BLINKIST_PASSWORD']
print('Logging into your Blinkist account... 💻')
print
req.submit()



req.set_handle_robots(False)
req.set_handle_equiv(False)
req.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
page = req.open("https://blinkist.com/api/books/library")
content = page.read()
x = json.loads(content)
print(x)

print('📚📚📚')
print('Blinkist Reading List')
print('📚📚📚')
print
for idx, v in enumerate(sorted(x['entries'].values())):
    if idx % 3 == 0:
        print('📚 Week: {}'.format(idx / 3 + 1))
    print('({}) {}'.format(
        idx+1, ' '.join([a.title() for a in v['slug'].split('-') if a != 'en'])
        )
    )
    print(slug)

page = req.response().read()
soup = BeautifulSoup(page, 'html.parser')
mydivs = soup.findAll("div", {"class": "book-card__title"})
#  for idx, d in enumerate(mydivs):
#    print('({}) {}'.format(idx + 1, d.text))
