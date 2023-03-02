from flask import current_app, make_response, request, Response, render_template, render_template_string, url_for, redirect, session
from database import dbop
from spider.videocms import get_all_video
from scheduler.scheduler import update_recommend_book_job, cmsUrl

_CMSAPI = '/cmsapi'

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
            return make_response({'res': True, 'videoCmsInfos': result})
        else:
            return make_response('NO', 403)
        
    @app.route(_CMSAPI + '/init/recommendbook', methods=['GET', 'POST'])
    def initRecommendBook():
        if session.get('admin') or session.get('token'):
            update_recommend_book_job()
            return make_response('YES')
        else:
            return make_response('NO', 403)
        
    @app.route(_CMSAPI + '/get/recommendbookcmsinfo', methods=['GET', 'POST'])
    def getRecommendBook():
        if session.get('admin') or session.get('token'):
            result = dbop.getAllRecommendBookCmsInfo()
            return make_response({'res': True, 'recommendBookCmsInfos': result})
        else:
            return make_response('NO', 403)
