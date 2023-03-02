import datetime
import time
import json
from flask_apscheduler import APScheduler

from spider.videocms import get_all_video
from spider.spider import book_recommend
from database.dbop import insertRecommendBook

scheduler = APScheduler()

cmsUrl = {
    "private": {
        "飞速资源": "https://www.feisuzyapi.com/api.php/provide/vod/from/fsm3u8/at/xmlsea/",
        "红牛资源": "https://www.hongniuzy2.com/api.php/provide/vod/from/hnm3u8/at/xml/",
        "八戒资源": "http://cj.bajiecaiji.com/inc/bjm3u8.php",
        "天空资源(未适配)": "https://m3u8.tiankongapi.com/api.php/provide/vod/from/tkm3u8/",
        "1080资源(未适配)": "https://api.1080zyku.com/inc/ldg_api_all.php"
    },
    "official": {
        "云解析资源": {
            "腾讯资源": "https://api.yparse.com/api/xml/qq",
            "爱奇艺": "https://api.yparse.com/api/xml/qiyi",
            "优酷": "https://api.yparse.com/api/xml/youku",
            "芒果": "https://api.yparse.com/api/xml/mgtv"
        }
    }
}

cmsUrlNames = {
    "private": ["飞速资源"],
    "official": {
        "云解析资源": ["腾讯资源", "爱奇艺", "优酷", "芒果"]
    }
}

# test minute='*', second='05,35'
@scheduler.task('cron', id='update_video', day='*', hour='3')
def update_video_job():
    for privateUrlName in cmsUrlNames["private"]:
        get_all_video(cmsUrl["private"][privateUrlName], "private", privateUrlName)
    for officialUrlName, officialUrlSiteNameList in cmsUrlNames["official"].items():
        for officialUrlSiteName in officialUrlSiteNameList:
            get_all_video(cmsUrl["official"][officialUrlName][officialUrlSiteName], "official", officialUrlName + "-" + officialUrlSiteName)
    print(str(datetime.datetime.now()) + ' Update Video Job executed')

@scheduler.task('cron', id='update_recommendBook', day='*', hour='*', minute='45')
def update_recommend_book_job():
    try:
        recommendBook = json.dumps(book_recommend())
        recommendBookDict = {}
        recommendBookDict["bookSource"] = "https://www.quge3.com"
        recommendBookDict["recommendBook"] = recommendBook
        recommendBookDict["lastUpdateTime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        insertRecommendBook(recommendBookDict)
        print(str(datetime.datetime.now()) + ' Update Recommend Book Job executed')
    except Exception as r:
        print('错误: %s' % (r))