import xml.etree.ElementTree as ET
import requests
import sys
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

sys.path.append(".")
from database import dbop

session = requests.session()
allcount = 0

def get_start_info(cmsUrl):
    global allcount
    print(cmsUrl, "开始了。。。")
    resp = session.get(cmsUrl, headers={ 'User-Agent': 'Chrome/98.0.4758.102 Safari/537.36' }, timeout=15)
    sourceData = resp.content.decode()
    root = ET.fromstring(sourceData, parser=ET.XMLParser(encoding="utf-8"))

    allcount = root.find('list').get('recordcount')
    pagecount = root.find('list').get('pagecount')
    print("影片总数：", allcount)

    classes = root.find('class')
    typeDict = {}
    for ty in classes.iter('ty'):
        typeDict[ty.get('id')] = ty.text
    return pagecount

def get_video_list(cmsUrl, pagecount, cmsType, urlName):
    global allcount
    with tqdm(total=int(allcount)) as pbar:
        pbar.set_description('当前影片数量：')
        with ThreadPoolExecutor(50) as t:
            for pg in range(int(pagecount), 0, -1):
                t.submit(get_video_and_insert, cmsUrl, pg, pbar, cmsType)
        videoCmsInfoDict = {}
        videoCmsInfoDict["name"] = urlName
        videoCmsInfoDict["isOfficial"] = "是" if cmsType == "official" else "否"
        videoCmsInfoDict["resourcesNums"] = pbar.n if pbar.n else 0
        videoCmsInfoDict["lastUpdateTime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        dbop.insertVideoCmsInfo(videoCmsInfoDict)

def get_video_and_insert(cmsUrl, pg, pbar, cmsType):
    try:
        resp = session.get(cmsUrl, headers={ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) ' }, params={'ac': "videolist", "pg": pg}, timeout=15)
        xmlData = resp.content.decode()
        root = ET.fromstring(xmlData)
        root = root.find('list')
        # pagesize = root.get('pagesize')
        # page = root.get('page')
        # recordcount = root.get('recordcount')
        videoDatas = []
        for video in root.iter('video'):
            if video.find('dl').find('dd') == None:
                continue
            videoData = {}
            videoData['id'], videoData['name'], videoData['type'], videoData['classification'], videoData['lastTime'], videoData['pic'], videoData['url'], videoData['lang'], videoData['area'], videoData['year'], videoData['note'], videoData['actor'], videoData['director'], videoData['des'] = video.find('id').text, video.find('name').text, video.find('type').text, video.find('tid').text, video.find('last').text, video.find('pic').text, video.find('dl').find('dd').text, video.find('lang').text, video.find('area').text, video.find('year').text, video.find('note').text, video.find('actor').text, video.find('director').text, video.find('des').text
            videoData['source'] = cmsUrl.split('/')[2]
            videoData['id'] = cmsUrl.split('/')[2].split('.')[1][:2] + videoData['id']
            if cmsType == "official":
                videoData['id'] += cmsUrl.split('/')[-1]
            videoDatas.append(videoData)
            # print(f"当前影片数量：{ count} / { allcount }。 影片名称：{ videoData['name'] }")
            pbar.update(1)
        dbop.insertVideos(videoDatas)
    except Exception as r:
        pbar.write('错误:  %s' % (r))


def get_all_video(cmsUrl, cmsType, urlName):
    pagecount = get_start_info(cmsUrl)
    get_video_list(cmsUrl, pagecount, cmsType, urlName)