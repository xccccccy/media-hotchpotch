import datetime
import time
from flask_apscheduler import APScheduler

from spider.videocms import get_all_video
from route.cms_route import cmsUrl

scheduler = APScheduler()
 
cmsUrlNames = {
    "private": ["飞速资源"],
    "official": {
        "云解析资源": ["腾讯资源", "爱奇艺", "优酷", "芒果"]
    }
}

@scheduler.task('cron', id='update_video', day='*', hour='3')
def update_video_job():
    for privateUrlName in cmsUrlNames["private"]:
        get_all_video(cmsUrl["private"][privateUrlName], "private", privateUrlName)
    for officialUrlName, officialUrlSiteNameList in cmsUrlNames["official"].items():
        for officialUrlSiteName in officialUrlSiteNameList:
            get_all_video(cmsUrl["official"][officialUrlName][officialUrlSiteName], "official", officialUrlName + "-" + officialUrlSiteName)
    print(str(datetime.datetime.now()) + ' Update Video Job executed')


