import logging
import inspect

import requests
import re

from bs4 import BeautifulSoup

session = requests.session()
quge3_url = 'https://www.quge3.com'
home_url = quge3_url
print('init session!')


def spider_decorator(func):
    def wrapTheFunction(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as r:
            logging.getLogger('MyWorld').error(f'- NET - {func.__name__} - {tuple(inspect.getargspec(func)[0])} - {args} - {r}')
            print(f'未知错误 %s' %(r))
            return None
    return wrapTheFunction

def test_connect():
    resp = session.get(home_url, headers=get_headers(), timeout=3)
    return resp.status_code

@spider_decorator
def book_search(search_string):
    search_resp = session.get(home_url + '/s', headers=get_headers(), params={'q': search_string}, timeout=5)
    search_bsobj = BeautifulSoup(search_resp.content.decode(), 'lxml')
    bookbox_list = search_bsobj.find('div', {'class': 'type_show'}).find_all('div', {'class': 'box'})
    result_list = []
    for bookbox in bookbox_list:
        a_bookbox_dict = {}
        book_id = bookbox.find('h4', {'class': 'bookname'}).find('a').get('href').split('/')[2]
        img_url = bookbox.find('img').get('src')
        author = bookbox.find('div', {'class': 'author'}).getText()[3:]
        resume = bookbox.find('div', {'class': 'uptime'}).getText()
        name = bookbox.find('h4', {'class': 'bookname'}).getText()
        a_bookbox_dict['name'] = name
        a_bookbox_dict['resume'] = resume
        a_bookbox_dict['author'] = author
        a_bookbox_dict['img_url'] = img_url
        a_bookbox_dict['book_id'] = book_id
        result_list.append(a_bookbox_dict)
    return result_list

@spider_decorator
def book_allinfo(book_id):
    info_dict = {}
    book_url = f'/book/{book_id}/'
    book_resp = session.get(home_url + book_url, headers=get_headers(), timeout=5)
    book_bsobj = BeautifulSoup(book_resp.content.decode(), 'lxml')

    catalogue_list_tag = book_bsobj.find('div', {'class': 'listmain'}).find_all(
        lambda e: e.name == 'dd' and 'class' not in e.attrs)
    catalogue_text_list = list(map(lambda x: x.getText(), catalogue_list_tag))
    catalogue_href_list = list(map(lambda x: x.find('a').get('href')[:-5], catalogue_list_tag))
    # catalogue_text_dict = dict(zip(range(len(catalogue_text_list)), catalogue_text_list))
    book_info = book_bsobj.find('div', {'class': 'info'})
    book_name = book_info.find('h1').getText()
    book_img_url = book_info.find('img').get('src')
    book_author = book_info.find('div', {'class': 'small'}).find('span').getText()[3:]
    book_resume = book_info.find('div', {'class': 'intro'}).getText()[7:]
    if book_resume[-8:] == ' 展开全部>> ':
        book_resume = book_info.find('div', {'class': 'intro'}).getText()[7:-8]
    info_dict['catalogue_text_list'] = catalogue_text_list
    info_dict['catalogue_href_list'] = catalogue_href_list
    info_dict['book_name'] = book_name
    info_dict['book_img_url'] = book_img_url
    info_dict['book_author'] = book_author
    info_dict['book_resume'] = book_resume
    info_dict['book_id'] = book_id
    return info_dict

@spider_decorator
def book_someinfo(book_id):
    info_dict = {}
    book_url = f'/book/{book_id}/'
    book_resp = session.get(home_url + book_url, headers=get_headers(), timeout=5)
    book_bsobj = BeautifulSoup(book_resp.content.decode(), 'lxml')
    book_info = book_bsobj.find('div', {'class': 'info'})
    book_name = book_info.find('h1').getText()
    book_img_url = book_info.find('img').get('src')
    book_author = book_info.find('div', {'class': 'small'}).find('span').getText()[3:]
    info_dict['book_name'] = book_name
    info_dict['book_img_url'] = book_img_url
    info_dict['book_author'] = book_author
    info_dict['book_id'] = book_id
    return info_dict

@spider_decorator
def book_content(book_id, catalogue_number):
    book_content_resp = session.get(home_url + f'/book/{book_id}/{catalogue_number}.html', headers=get_headers(), timeout=5)
    book_content_bsobj = BeautifulSoup(book_content_resp.content.decode(), 'lxml')
    book_catalogue_name = book_content_bsobj.find('div', {'class': 'content'}).find('h1').getText()
    context_0 = re.findall(r'.*?id="chaptercontent">+(.*?)\n+',
                           str(book_content_bsobj.find('div', {'id': 'chaptercontent'})).replace('\u3000', ' '))[0].replace(' ', '&emsp;').replace("请收藏本站：https://www.quge3.com。笔趣阁手机版：https://m.quge3.com", "").replace(".quge3.", "")
    return {'catalogue_name': book_catalogue_name, 'content': context_0}


def get_headers():
    UA = [
          "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
          "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
          "Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0",
          "Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0",
          "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
          "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
          "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
          "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
          "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7",
          "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
          "Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0",
          "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
          "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0",
          "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0",
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
          "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0",
          "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
          "Mozilla/5.0 (Windows NT 5.1; rv:30.0) Gecko/20100101 Firefox/30.0",
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
          "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
          "Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0",
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0",
          "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
          "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0",
          "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
          "Chrome/98.0.4758.102 Safari/537.36"
          ]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/98.0.4758.102 Safari/537.36'  # random.choice(UA),
    }
    return headers
