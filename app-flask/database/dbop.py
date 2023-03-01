import sys
import os
basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(basedir)

from db import db, init_db, User, Bookshelf, Video, VideoCmsInfo, RecommendBookCmsInfo
from flask import Flask, current_app, session
from sqlalchemy import or_,and_

app = None


def init_database(_app):
    global app
    app = _app
    init_db(_app)
    with app.app_context():
        current_app.logger.info('- DB - Init Database.')


def insertUser(id, name, passwd, face_id=False):
    with app.app_context():
        try:
            user = User(id, name, passwd, face_id)
            db.session.add(user)
            db.session.commit()
            return {'res': True}
        except Exception as r:
            print('错误: %s' % (r))
            return {'res': False, 'context': "已经存在该id相关用户。"}


def queryUser(user_id):
    with app.app_context():
        try:
            data = User.query.get(user_id)
            user = {'id': data.id, 'name': data.name, 'face_id': data.face_id, 'icon': data.icon_url}
            return {'res': True, 'user': user}
        except Exception as r:
            print('错误:  %s' % (r))
            return {'res': False, 'context': "不存在该id相关用户。"}


def delUser(user_id):
    with app.app_context():
        try:
            user = User.query.get(user_id)
            db.session.delete(user)
            db.session.commit()
            return {'res': True, 'context': f'删除用户{user_id}成功'}
        except Exception as r:
            print('错误:  %s' % (r))
            return {'res': False, 'context': "不存在该id相关用户。"}


def updateUser(user_id, face_id):
    with app.app_context():
        try:
            user = User.query.get(user_id)
            user.face_id = face_id
            db.session.add(user)
            db.session.commit()
            return {'res': True, 'context': '更新user成功。'}
        except Exception as r:
            print('错误:  %s' % (r))
            return {'res': False, 'context': "不存在该id相关用户。"}


def userLogin(user_id, passwd):
    with app.app_context():
        try:
            user = User.query.get(user_id)
            if user.passwd == passwd:
                return {'res': True, 'context': '登录成功。', 'user_name': user.name, 'faceid': user.face_id, 'icon': user.icon_url }
            else:
                return {'res': False, 'context': "密码错误。"}
        except Exception as r:
            print('错误:  %s' % (r))
            return {'res': False, 'context': "不存在该id相关用户。"}


def queryBookshelf(user_id):
    with app.app_context():
        try:
            user_id = User.query.get(user_id).id
            bookshelf = Bookshelf.query.get(user_id)
            if bookshelf:
                return {'res': True, 'bookshelf': bookshelf.bookshelf}
            else:
                bookshelf = Bookshelf(user_id, '{}')
                db.session.add(bookshelf)
                db.session.commit()
                return {'res': True, 'bookshelf': '{}'}
        except Exception as r:
            print('错误:  %s' % (r))
            return {'res': False, 'context': "不存在该id相关用户。"}


def updateBookshelf(user_id, _bookshelf):
    with app.app_context():
        try:
            user_id = User.query.get(user_id).id
            bookshelf = Bookshelf.query.get(user_id)
            if bookshelf:
                bookshelf.bookshelf = _bookshelf
                db.session.add(bookshelf)
                db.session.commit()
            else:
                bookshelf = Bookshelf(user_id, _bookshelf)
                db.session.add(bookshelf)
                db.session.commit()
            return {'res': True, 'context': '更新书架成功。'}
        except Exception as r:
            print('错误:  %s' % (r))
            return {'res': False, 'context': "不存在该id相关用户。"}


def insertVideo(id, name, type, classification, lastTime, pic, url, lang, area, year, note, actor, director, des, source):
    with app.app_context():
        try:
            video = Video.query.get(id)
            if video:
                video_dict = dict(zip(["id", "name", "type", "classification", "lastTime", "pic", "url", "lang", "area", "year", "note", "actor", "director", "des", "source"], [id, name, type, classification, lastTime, pic, url, lang, area, year, note, actor, director, des, source]))
                _updateVideo(video, video_dict)
            else:
                video = Video(id, name, type, classification, lastTime, pic, url, lang, area, year, note, actor, director, des, source)
                db.session.add(video)
            db.session.commit()
            return {'res': True}
        except Exception as r:
            print('错误: %s' % (r))
            return {'res': False, 'context': "已经存在该id。"}


def _updateVideo(video, videoData):
    video.name, video.type, video.classification, video.lastTime, video.pic, video.url, video.lang, video.area, video.year, video.note, video.actor, video.director, video.des, video.source = videoData['name'], videoData['type'], videoData['classification'], videoData['lastTime'], videoData['pic'], videoData['url'], videoData['lang'], videoData['area'], videoData['year'], videoData['note'], videoData['actor'], videoData['director'], videoData['des'], videoData['source']

def insertVideos(VideoDatas):
    with app.app_context():
        try:
            for videoData in VideoDatas:
                video = Video.query.get(videoData['id'])
                if video:
                    _updateVideo(video, videoData)
                else:
                    id, name, type, classification, lastTime, pic, url, lang, area, year, note, actor, director, des, source = videoData['id'], videoData['name'], videoData['type'], videoData['classification'], videoData['lastTime'], videoData['pic'], videoData['url'], videoData['lang'], videoData['area'], videoData['year'], videoData['note'], videoData['actor'], videoData['director'], videoData['des'], videoData['source']
                    video = Video(id, name, type, classification, lastTime, pic, url, lang, area, year, note, actor, director, des, source)
                    db.session.add(video)
            db.session.commit()
            return {'res': True}
        except Exception as r:
            print('错误: %s' % (r))
            return {'res': False, 'context': "已经存在该id。"}


def delAllVideos():
    with app.app_context():
        try:
            db.session.query(Video).delete()
            db.session.commit()
            return {'res': True}
        except Exception as r:
            print('错误: %s' % (r))
            return {'res': False, 'context': "删除失败"}


def searchVideo(searchString):
    with app.app_context():
        try:
            video_filter = {
                or_(
                    Video.name.ilike(f'%{searchString}%'),
                    Video.actor.ilike(f'%{searchString}%')
                )
            }
            objs = Video.query.filter(*video_filter).all()
            objs = list(map(lambda x: x.to_dict(),objs))
            objs = sorted(objs, key=lambda x:((x["name"].index(searchString) if x["name"] != searchString else -1) if searchString in x["name"] else x["actor"].index(searchString), (len(x["name"]) if x["name"].index(searchString) == 0 else x["name"].index(searchString)) if searchString in x["name"] else x["actor"].index(searchString)))[:50]
            return {'res': True, 'videos': objs}
        except Exception as r:
            print('错误:  %s' % (r))
            return {'res': False, 'context': "出现错误。"}



def insertVideoCmsInfo(videoCmsInfoDict):
    with app.app_context():
        try:
            videoCmsInfo = VideoCmsInfo.query.get(videoCmsInfoDict["name"])
            if videoCmsInfo:
                videoCmsInfo.name, videoCmsInfo.isOfficial, videoCmsInfo.resourcesNums, videoCmsInfo.lastUpdateTime = videoCmsInfoDict["name"], videoCmsInfoDict["isOfficial"], videoCmsInfoDict["resourcesNums"], videoCmsInfoDict["lastUpdateTime"]
            else:
                videoCmsInfo = VideoCmsInfo(videoCmsInfoDict["name"], videoCmsInfoDict["isOfficial"], videoCmsInfoDict["resourcesNums"], videoCmsInfoDict["lastUpdateTime"])
                db.session.add(videoCmsInfo)
            db.session.commit()
            return {'res': True}
        except Exception as r:
            print('错误: %s' % (r))
            return {'res': False, 'context': "发生未知错误"}


def getAllVideoCmsInfo():
    with app.app_context():
        try:
            objs = VideoCmsInfo.query.all()
            objs = list(map(lambda x: x.to_dict(), objs))[:100]
            return {'res': True, 'videoCmsInfos': objs}
        except Exception as r:
            print('错误: %s' % (r))
            return {'res': False, 'context': "发生未知错误"}

def insertRecommendBook(recommendBookDict):
    with app.app_context():
        try:
            recommendBookCmsInfo = RecommendBookCmsInfo.query.get(recommendBookDict["bookSource"])
            if recommendBookCmsInfo:
                recommendBookCmsInfo.bookSource, recommendBookCmsInfo.recommendBook, recommendBookCmsInfo.lastUpdateTime = recommendBookDict["bookSource"], recommendBookDict["recommendBook"], recommendBookDict["lastUpdateTime"]
            else:
                recommendBookCmsInfo = RecommendBookCmsInfo(recommendBookDict["bookSource"], recommendBookDict["recommendBook"], recommendBookDict["lastUpdateTime"])
                db.session.add(recommendBookCmsInfo)
            db.session.commit()
            return {'res': True}
        except Exception as r:
            print('错误: %s' % (r))
            return {'res': False, 'context': "发生未知错误"}
        
def getRecommendBook(bookSource):
    with app.app_context():
        try:
            recommendBookCmsInfo = RecommendBookCmsInfo.query.get(bookSource)
            return recommendBookCmsInfo.recommendBook
        except Exception as r:
            print('错误: %s' % (r))
            return None
        
        
if __name__ == "__main__":
    app=Flask('11')
    init_database(app)
    print(searchVideo("功夫"))
    # app.run(debug=True, host='0.0.0.0', port=5002)
