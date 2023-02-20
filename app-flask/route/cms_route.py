from flask import current_app, make_response, request, Response, render_template, render_template_string, url_for, redirect, session
from database import dbop
from spider.videocms import get_all_video

_CMSAPI = '/cmsapi'

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


def initCmsRoute(app):
    @app.route(_CMSAPI + '/init/videos', methods=['GET', 'POST'])
    def downloadvideos():
        if session.get('admin') or session.get('token'):
            cmsUrlNames = request.json['cmsUrlName']
            print(cmsUrlNames)
            for privateUrlName in cmsUrlNames["private"]:
                get_all_video(cmsUrl["private"][privateUrlName], "private", privateUrlName)
            if type(cmsUrlNames["official"]) == dict:
                for officialUrlName, officialUrlSiteNameList in cmsUrlNames["official"].items():
                    for officialUrlSiteName in officialUrlSiteNameList:
                        get_all_video(cmsUrl["official"][officialUrlName][officialUrlSiteName], "official", officialUrlName + "-" + officialUrlSiteName)
            return make_response('YES')
        else:
            return make_response('NO', 403)

    @app.route(_CMSAPI + '/init/urlnames', methods=['GET', 'POST'])
    def initUrlNames():
        if session.get('admin') or session.get('token'):
            return make_response({ 
                "data": {
                    "private": list(cmsUrl["private"].keys()),
                    "official": dict(zip(list(cmsUrl["official"].keys()), [list(v.keys()) for k, v in cmsUrl["official"].items()])),
                }})
        else:
            return make_response('NO', 403)

    @app.route(_CMSAPI + '/del/allvideos', methods=['GET', 'POST'])
    def delAllVideos():
        if session.get('admin') or session.get('token'):
            dbop.delAllVideos()
            return make_response("YES")
        else:
            return make_response('NO', 403)

    @app.route(_CMSAPI + '/get/allcmsinfos', methods=['GET', 'POST'])
    def getAllVideoCmsInfos():
        if session.get('admin') or session.get('token'):
            result = dbop.getAllVideoCmsInfo()
            return make_response(result)
        else:
            return make_response('NO', 403)
