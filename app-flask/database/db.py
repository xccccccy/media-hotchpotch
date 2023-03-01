import os
from flask import current_app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64))
    passwd = db.Column(db.String(64))
    face_id = db.Column(db.Boolean)
    icon_url = db.Column(db.String(64))

    def __init__(self, id, name, passwd, face_id=False, icon_url="/static/icon/user/default.png"):
        self.id = id
        self.name = name
        self.passwd = passwd
        self.face_id = face_id
        self.icon_url = icon_url

    def __repr__(self):
        return '< User: %s >' % self.name

class VideoClassification(db.Model):
    __tablename__ = 'VideoClassification'
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64))

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '< VideoClassification: %s >' % self.name


class Bookshelf(db.Model):
    # 定义表名
    __tablename__ = 'Bookshelfs'
    # 定义列对象
    id = db.Column(db.String(64), db.ForeignKey('Users.id'),  primary_key=True)
    bookshelf = db.Column(db.String(1024))

    def __init__(self, id, bookshelf):
        self.id = id
        self.bookshelf = bookshelf

    # repr()方法显示一个可读字符串
    def __repr__(self):
        return '<Bookshelf ->  User_id:%s, Bookshelf:%s >' % self.id, self.bookshelf
    
class RecommendBookCmsInfo(db.Model):
    __tablename__ = 'RecommendBookCmsInfo'
    bookSource = db.Column(db.String(64), primary_key=True)
    recommendBook = db.Column(db.String(64))
    lastUpdateTime = db.Column(db.String(64))

    def __init__(self, bookSource, recommendBook, lastUpdateTime):
        self.bookSource = bookSource
        self.recommendBook = recommendBook
        self.lastUpdateTime = lastUpdateTime

    def __repr__(self):
        return '< RecommendBookCmsInfo: %s >' % self.name

    def to_dict(self):
        return {c.name: getattr(self, c.name) if getattr(self, c.name) else "" for c in self.__table__.columns}

class Video(db.Model):
    # 定义表名
    __tablename__ = 'VideoList'
    # 定义列对象
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64))
    type = db.Column(db.String(64))
    classification = db.Column(db.String(64))
    lastTime = db.Column(db.String(64))
    pic = db.Column(db.String(64))
    url = db.Column(db.String(64))
    lang = db.Column(db.String(64))
    area =db.Column(db.String(64))
    year = db.Column(db.String(64))
    note = db.Column(db.String(64))
    actor = db.Column(db.String(64))
    director = db.Column(db.String(64))
    des = db.Column(db.String(64))
    source = db.Column(db.String(64))


    # repr()方法显示一个可读字符串
    def __init__(self, id, name, type, classification, lastTime, pic, url, lang, area, year, note, actor, director, des, source):
        self.id = id
        self.name = name
        self.type = type
        self.classification = classification
        self.lastTime = lastTime
        self.pic = pic
        self.url = url
        self.lang = lang
        self.area = area
        self.year = year
        self.note = note
        self.actor = actor
        self.director = director
        self.des = des
        self.source = source

    def __repr__(self):
        return '< Video: %s >' % self.name
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) if getattr(self, c.name) else "" for c in self.__table__.columns}

class VideoCmsInfo(db.Model):
    __tablename__ = 'VideoCmsInfo'
    name = db.Column(db.String(64), primary_key=True)
    isOfficial = db.Column(db.String(64))
    resourcesNums = db.Column(db.String(64))
    lastUpdateTime = db.Column(db.String(64))

    def __init__(self, name, isOfficial, resourcesNums, lastUpdateTime):
        self.name = name
        self.isOfficial = isOfficial
        self.resourcesNums = resourcesNums
        self.lastUpdateTime = lastUpdateTime

    def __repr__(self):
        return '< VideoClassification: %s >' % self.name

    def to_dict(self):
        return {c.name: getattr(self, c.name) if getattr(self, c.name) else "" for c in self.__table__.columns}

def init_db(app):
    basedir = os.path.abspath(os.path.dirname(__file__))
    # 设置连接数据库的URL
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + \
        os.path.join(basedir, "data.sqlite")

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 查询时会显示原始SQL语句
    app.config['SQLALCHEMY_ECHO'] = False

    with app.app_context():
        db.init_app(app)
        if not os.path.exists(os.path.join(basedir, "data.sqlite")):
            db.create_all()
            current_app.logger.info(f'- DB - Database Create all.')
        else:
            db.create_all()
            # print(db.engine)

# def add_column(engine, table_name, column):
#     column_name = column.compile(dialect=engine.dialect)
#     column_type = column.type.compile(engine.dialect)
#     engine.execute('ALTER TABLE %s ADD COLUMN %s %s' % (table_name, column_name, column_type))

# column = Column('new_column_name', String(100), primary_key=True)
# add_column(engine, table_name, column)