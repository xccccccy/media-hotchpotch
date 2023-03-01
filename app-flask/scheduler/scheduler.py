import datetime
import time
import json
from flask_apscheduler import APScheduler

from spider.videocms import get_all_video
from spider.spider import book_recommend
from route.cms_route import cmsUrl
from database.dbop import insertRecommendBook

scheduler = APScheduler()
 
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

@scheduler.task('cron', id='update_recommendBook', day='*', hour='3')
def update_recommend_book_job():
    recommendBook = json.dumps(book_recommend())
    recommendBookDict = {}
    recommendBookDict["bookSource"] = "https://www.quge3.com"
    recommendBookDict["recommendBook"] = recommendBook
    recommendBookDict["lastUpdateTime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    insertRecommendBook(recommendBookDict)
    print(str(datetime.datetime.now()) + ' Update Recommend Book Job executed')
