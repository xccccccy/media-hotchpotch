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
            logging.getLogger('MyWorld').error(f'- NET - {func.__name__} - {tuple(inspect.getfullargspec(func)[0])} - {args} - {r}')
            print(f'未知错误 %s' %(r))
            return None
    return wrapTheFunction

def test_connect():
    resp = session.get(home_url, headers=get_headers(), timeout=3)
    return resp.status_code


# book 相关的

@spider_decorator
def book_recommend():
    recommend_books = {'hot_book': [], 'top_book': [], 'type_book': {}}
    book_resp = session.get(home_url, headers=get_headers(), timeout=10)
    book_bsobj = BeautifulSoup(book_resp.content.decode(), 'lxml')
    hot_book_bsobj = book_bsobj.find('div', {'class': 'hot'}).find_all('div', {'class': 'item'})
    top_book_bsobj = book_bsobj.find('div', {'class': 'top'}).find_all('li')

    hot_book = []
    for book_li in hot_book_bsobj:
        a_book = {
            'name': book_li.find('dl').find('a').getText(),
            'author': book_li.find('dl').find('span').getText(),
            'img_url': book_li.find('img').get('src'),
            'resume': book_li.find('dd').getText().replace('\u3000', ''),
            'book_id': book_li.find('dl').find('a').get('href').split('/')[2]
        }
        hot_book.append(a_book)
    recommend_books['hot_book'] = hot_book

    top_book = []
    for book_li in top_book_bsobj:
        a_book = {
            'name': book_li.find('span', {'class': 's2'}).getText(),
            'type': book_li.find('span', {'class': 's1'}).getText()[1:-1],
            'author': book_li.find('span', {'class': 's5'}).getText(),
            'book_id': book_li.find('a').get('href').split('/')[2]
        }
        top_book.append(a_book)
    recommend_books['top_book'] = top_book

    for book_block in book_bsobj.find_all('div', {'class': 'block'}):
        book_type = book_block.find('h2').getText()
        block_top_book = {
            'name': book_block.find('div', {'class', 'block_top'}).find('dl').find('a').getText(),
            'resume': book_block.find('div', {'class', 'block_top'}).find('dd').getText()[3:].replace('\u3000', ''),
            'img_url': book_block.find('div', {'class', 'block_top'}).find('img').get('src'),
            'book_id': book_block.find('div', {'class', 'block_top'}).find('dl').find('a').get('href').split('/')[2]
        }
        block_other_books = []
        for book_li in book_block.find_all('li'):
            a_book = {
                'name': book_li.find('span', {'class': 's2'}).getText(),
                'type': book_li.find('span', {'class': 's1'}).getText()[1:-1],
                'author': book_li.find('span', {'class': 's3'}).getText(),
                'book_id': book_li.find('a').get('href').split('/')[2]
            }
            block_other_books.append(a_book)
        recommend_books['type_book'][book_type] = {
            'block_top_book': block_top_book,
            'block_other_books': block_other_books
        }
    
    return recommend_books


@spider_decorator
def book_search(search_string):
    search_resp = session.get(home_url + '/s', headers=get_headers(), params={'q': search_string}, timeout=10)
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
        if '肏' in name or '淫' in name or '操' in name or '艹' in name or '艳' in name or '女' in name or '逼' in name or '勾引' in name or '尿' in name or '干' in name or '快穿' in name or '床' in name:
            continue
        if '肉' in name or '撞坏' in name or '骚' in name or '乱伦' in name or '丈' in name or '岳母' in name or '矫' in name:
            continue
        if '母' in name or '射' in name or '弄哭' in name or '强睡' in name:
            continue
        if len(re.findall(re.compile(r'[A-Za-z]', re.S), name)):
            continue
        a_bookbox_dict['name'] = name
        a_bookbox_dict['resume'] = resume.replace('\u3000', '')
        a_bookbox_dict['author'] = author
        a_bookbox_dict['img_url'] = img_url
        a_bookbox_dict['book_id'] = book_id
        result_list.append(a_bookbox_dict)
    return result_list

@spider_decorator
def book_allinfo(book_id):
    info_dict = {}
    book_url = f'/book/{book_id}/'
    book_resp = session.get(home_url + book_url, headers=get_headers(), timeout=10)
    book_bsobj = BeautifulSoup(book_resp.content.decode(), 'lxml')

    catalogue_list_tag = book_bsobj.find('div', {'class': 'listmain'}).find_all(
        lambda e: e.name == 'dd' and 'class' not in e.attrs)
    catalogue_text_list = list(map(lambda x: x.getText(), catalogue_list_tag))
    catalogue_href_list = list(map(lambda x: x.find('a').get('href')[:-5], catalogue_list_tag))
    # catalogue_text_dict = dict(zip(range(len(catalogue_text_list)), catalogue_text_list))
    book_type = book_bsobj.find('div', {'class': 'path'}).getText().split('>')[1].strip()
    book_info = book_bsobj.find('div', {'class': 'info'})
    book_name = book_info.find('h1').getText()
    book_img_url = book_info.find('img').get('src')
    book_author = book_info.find('div', {'class': 'small'}).find_all('span')[0].getText()[3:]
    book_state = book_info.find('div', {'class': 'small'}).find_all('span')[1].getText()[3:]
    book_last_update_time = book_info.find('div', {'class': 'small'}).find_all('span')[2].getText()[3:]
    book_last_catalogue_text = book_info.find('div', {'class': 'small'}).find_all('span')[3].getText()[3:]
    book_resume = book_info.find('div', {'class': 'intro'}).getText()[7:]
    if book_resume[-8:] == ' 展开全部>> ':
        book_resume = book_info.find('div', {'class': 'intro'}).getText()[7:-8]
    info_dict['catalogue_text_list'] = catalogue_text_list
    info_dict['catalogue_href_list'] = catalogue_href_list
    info_dict['book_name'] = book_name
    info_dict['book_type'] = book_type
    info_dict['book_img_url'] = book_img_url
    info_dict['book_author'] = book_author
    info_dict['book_state'] = book_state
    info_dict['book_last_update_time'] = book_last_update_time
    info_dict['book_last_catalogue_text'] = book_last_catalogue_text
    info_dict['book_resume'] = book_resume.replace('\u3000', '')
    info_dict['book_id'] = book_id
    return info_dict

@spider_decorator
def book_someinfo(book_id):
    info_dict = {}
    book_url = f'/book/{book_id}/'
    book_resp = session.get(home_url + book_url, headers=get_headers(), timeout=10)
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
    book_content_resp = session.get(home_url + f'/book/{book_id}/{catalogue_number}.html', headers=get_headers(), timeout=10)
    book_content_bsobj = BeautifulSoup(book_content_resp.content.decode(), 'lxml')
    book_catalogue_name = book_content_bsobj.find('div', {'class': 'content'}).find('h1').getText()
    context_0 = re.findall(r'.*?id="chaptercontent">+(.*?)\n+',
                           str(book_content_bsobj.find('div', {'id': 'chaptercontent'})).replace('\u3000', ' '))[0].replace(' ', '&emsp;').replace("请收藏本站：https://www.quge3.com。笔趣阁手机版：https://m.quge3.com", "").replace(".quge3.", "")
    return {'catalogue_name': book_catalogue_name, 'content': context_0}


# video 相关的
@spider_decorator
def web_video_search(search_string):
    aiqiyi_videos = aiqiyi_video_search(search_string)
    return aiqiyi_videos + []

# @spider_decorator
def aiqiyi_video_search(search_string):
    search_resp = session.get("https://so.iqiyi.com/so" + '/q_' + search_string, headers=get_headers(), timeout=10)
    search_bsobj = BeautifulSoup(search_resp.content.decode(), 'lxml')

    result_items = search_bsobj.find_all('div', {'class': 'qy-search-result-item'})
    all_videos = []
    all_videos_type = []
    for item in result_items:
        item_type_bsobj = item.find('span', {'class': 'item-type'})
        if item_type_bsobj:
            all_videos_type.append(item_type_bsobj.getText())
            if item_type_bsobj.getText() in ["电视剧", "电影", "综艺"]:
                video = {}
                video['type'] = item.find('span', {'class': 'item-type'}).getText()
                video['name'] = item.find('a', {'class': 'main-tit'}).get('title')
                video['pic'] = "https://" + item.find('div', {'class': 'qy-mod-img'}).find('source').get('srcset').split('?')[0][2:]
                video['year'] = item.find('em', {'class': 'year'}).getText()
                for info in item.findAll('div', {'class': 'qy-search-result-info multiple'}):
                    info_type = info.find('label').getText()
                    if info_type == "简介:":
                        video['des'] = info.find('span').get('title')
                        video['video_url'] = "https://" + info.find('a').get('href')[2:]
                        break
                if item_type_bsobj.getText() not in ["综艺"]:
                    video['note'] = item.find('span', {'class': 'qy-mod-label'}).getText()
                    for info in item.findAll('div', {'class': 'qy-search-result-info half'}):
                        info_type = info.find('label').getText()
                        if info_type == "导演:":
                            video['director'] = ','.join([actor.getText() for actor in info.findAll('a')])
                        elif info_type == "主演:":
                            video['actor'] = ','.join([actor.getText() for actor in info.findAll('a')])
                all_videos.append(video)

    all_videourls = []
    for script_bsobj in search_bsobj.findAll('script'):
        if "cardData" in script_bsobj.getText():
            script_urls_str = script_bsobj.getText()
            break
    script_videoinfo_items_str = re.match('.*?list:\[(.*?})],sear', script_urls_str).group(1).replace('\n', '').replace(' ', '')
    script_videoinfo_items = script_videoinfo_items_str.split(',{id:')
    j = 0
    for i in range(len(script_videoinfo_items)):
        videoinfo_item_str = script_videoinfo_items[i]
        if "tag:" in videoinfo_item_str:
            match_result = re.match(r'.*?tag:"(.*?)"', videoinfo_item_str)
            if match_result:
                video_type = match_result.group(1)
            else:
                if j >= len(all_videos_type):
                    continue
                video_type = all_videos_type[j]
            if video_type in ["电视剧", "综艺"]:
                urls = []
                videoinfos_list = re.findall(r"\{(.*?)}", re.match(r".*?videoinfos:\[(.*?)],", videoinfo_item_str.replace('\\u002F', '/')).group(1))
                for video_info in videoinfos_list:
                    video_url = re.match(r'.*?,url:"(.*?)"', video_info)
                    video_name = re.match(r'.*?name:"(.*?)"', video_info)
                    urls.append({"name": video_name.group(1) if video_name else "", "url": "https://" + video_url.group(1)[2:] if video_url else ""})
                all_videourls.append(urls)
            elif video_type == "电影":
                all_videourls.append("")
            elif video_type in ["小说", "知识", "动漫"]:
                pass
            j += 1

    for i in range(len(all_videos)):
        if all_videos[i]['type'] in ["电视剧", "综艺"]:
            videourls = all_videourls[i]
            if videourls[0]["url"] == "":
                videourls[0]["url"] = all_videos[i]["video_url"]
            for j in range(len(videourls)):
                url_item = videourls[j]
                if not url_item['name']:
                    videourls[j]['name'] = all_videos[i]["name"] + f" 第{j + 1}集"
            # all_videos[i]["urls"] = videourls
            all_videos[i]["url"] = "#".join([f"{videourl['name']}${videourl['url']}$qiyi" for videourl in videourls])
        else:
            all_videos[i]["url"] = f"HD${all_videos[i]['video_url']}$qiyi"
        del all_videos[i]['video_url']
        # del all_videos[i]['urls']
        
    return all_videos

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


if __name__ == "__main__":
    print(aiqiyi_video_search("开工了"))