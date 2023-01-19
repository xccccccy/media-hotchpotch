import json
import os
import datetime

from flask import current_app, make_response, request, Response, render_template, render_template_string, url_for, redirect, session
from spider import spider
from face_recognize import face_recognize_component
from database import dbop
from mail.mail import generate_verification_code, send_message
from .scm_router import initScmRoute
from .cms_route import initCmsRoute
from .video_route import initVideoRoute


def init_route(app):

    with app.app_context():
        current_app.logger.info('- NET - Init Route.')
    app.secret_key = r'F12Zr47j\3yX R~X@H!jLwf/T'
    _API = '/api'
    _FACEAPI = '/faceapi'
    config_dict = {}
    if not os.path.exists('config/allconfig.json'):
        with open('config/allconfigtemplate.json', 'r', encoding='utf-8') as f:
            config_dict = json.load(f)
        with open('config/allconfig.json', 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=3)
    else:
        with open('config/allconfig.json', 'r', encoding='utf-8') as f:
            config_dict = json.load(f)
        
    @app.route(_API + '/book/search', methods=['GET', 'POST'])
    def book_search():
        search_string = request.json['search_string']
        temp = spider.book_search(search_string)
        if temp or len(temp) == 0:
            res = make_response({'data': temp})
        else:
            res = make_response('NO', 500)
        current_app.logger.info(
            f'- NET - {request.remote_addr} - {request.full_path} - {res.status_code} - {search_string}')
        return res

    @app.route(_API + '/bookinfo/<int:book_id>')
    def book_info(book_id):
        book_infos = spider.book_allinfo(book_id)
        if book_infos:
            res = make_response(book_infos)
        else:
            res = make_response('NO', 500)
        current_app.logger.info(
            f'- NET - {request.remote_addr} - {request.full_path} - {res.status_code}')
        return res

    @app.route(_API + '/bookinfo2/<int:book_id>')
    def book_info2(book_id):
        book_infos = spider.book_someinfo(book_id)
        if book_infos:
            res = make_response(book_infos)
        else:
            res = make_response('NO', 500)
        current_app.logger.info(
            f'- NET - {request.remote_addr} - {request.full_path} - {res.status_code}')
        return res

    @app.route(_API + '/content/<int:book_id>/<int:content_id>')
    def book_content(book_id, content_id):
        temp = spider.book_content(book_id, content_id)
        if temp:
            res = make_response(temp)
        else:
            res = make_response('NO', 500)
        current_app.logger.info(
            f'- NET - {request.remote_addr} - {request.full_path} - {res.status_code}')
        return res

    @app.route(_FACEAPI + '/facerecognition', methods=['GET', 'POST'])
    def api_face_recognize():  # 考虑同步问题
        if not config_dict['openLogin']['if']:
            return make_response({'res': False, 'context': '已经关闭登录功能！', 'type': False})
        if not config_dict['openFacerecognize']['if']:
            return make_response({'res': False, 'context': '已经关闭人脸登录功能！', 'type': False})
        img_base64 = request.json['img_base64'].split(',')[1]
        hasface, face_id = face_recognize_component.recognize(img_base64)
        if not face_id:
            res = Response(json.dumps(
                {'res': False, 'hasface': hasface}), mimetype='application/json')
        else:
            user = dbop.queryUser(face_id)['user']
            res = Response(json.dumps({'res': True, 'id': face_id, 'name': user['name'], 'icon':user['icon']}), mimetype='application/json')
        face_id = face_id if face_id else 'None'
        current_app.logger.info(
            f'- NET - {request.remote_addr} - {request.full_path} - {res.status_code} - {face_id}')
        return res

    @app.route(_FACEAPI + '/addfacerecognition', methods=['GET', 'POST'])
    def api_add_face_recognize():  # 考虑同步问题
        if not config_dict['openFacerecognize']['if']:
            return make_response({'res': False, 'context': '已经关闭添加 FaceID 功能！', 'type': False})
        img_base64s = request.json['img_base64s']
        face_id = request.json['face_id']
        if face_recognize_component.add_face_recognize(img_base64s, face_id):
            dbop.updateUser(face_id, True)
            res_add_face = True
        else:
            res_add_face = False
        res = Response(json.dumps({'res': res_add_face}),
                       mimetype='application/json')
        current_app.logger.info(
            f'- NET - {request.remote_addr} - {request.full_path} - {res.status_code} - {face_id} - {res_add_face}')
        return res

    @app.route(_API + '/insertuser', methods=['GET', 'POST'])
    def insertuser():
        if config_dict['openLogon']['value'] == "close":
            return make_response({'res': False, 'context': '已经关闭注册功能！', 'type': False})
        _id = request.json['id']
        _name = request.json['name']
        _passwd = request.json['passwd']
        _face_id = False
        res = Response(json.dumps(dbop.insertUser(
            _id, _name, _passwd, _face_id)), mimetype='application/json')
        current_app.logger.info(
            f'- NET - {request.remote_addr} - {request.full_path} - {res.status_code} - {_id} - {_name}')
        return res

    @app.route(_API + '/queryuser', methods=['GET', 'POST'])
    def queryuser():
        _id = request.json['id']
        res = Response(json.dumps(dbop.queryUser(_id)),
                       mimetype='application/json')
        current_app.logger.info(
            f'- NET - {request.remote_addr} - {request.full_path} - {res.status_code} - {_id}')
        return res

    @app.route(_API + '/updateuser', methods=['GET', 'POST'])
    def updateuser():
        _id = request.json['id']
        _face_id = request.json['faceid']
        res = Response(json.dumps(dbop.updateUser(_id, _face_id)),
                       mimetype='application/json')
        current_app.logger.info(
            f'- NET - {request.remote_addr} - {request.full_path} - {res.status_code} - {_id}')
        return res

    @app.route(_API + '/login', methods=['GET', 'POST'])
    def login():
        if not config_dict['openLogin']['if']:
            return make_response({'res': False, 'context': '已经关闭登录功能！', 'type': False})
        _id = request.json['id']
        _passwd = request.json['passwd']
        res = Response(json.dumps(dbop.userLogin(_id, _passwd)),
                       mimetype='application/json')
        current_app.logger.info(
            f'- NET - {request.remote_addr} - {request.full_path} - {res.status_code} - {_id}')
        return res

    @app.route(_API + '/querybookshelf', methods=['GET', 'POST'])
    def queryquerybookshelfuser():
        _id = request.json['id']
        res = Response(json.dumps(dbop.queryBookshelf(_id)),
                       mimetype='application/json')
        current_app.logger.info(
            f'- NET - {request.remote_addr} - {request.full_path} - {res.status_code} - {_id}')
        return res

    @app.route(_API + '/updatebookshelf', methods=['GET', 'POST'])
    def updateBookshelf():
        _id = request.json['id']
        _bookshelf = request.json['bookshelf']
        res = Response(json.dumps(dbop.updateBookshelf(
            _id, _bookshelf)), mimetype='application/json')
        current_app.logger.info(
            f'- NET - {request.remote_addr} - {request.full_path} - {res.status_code} - {_id} - {_bookshelf}')
        return res

    @app.route(_API + '/verification', methods=['GET', 'POST'])
    def all_config():
        remote_verification_code = request.json['verification_code']
        request_type = request.json['type']
        if request_type == 'get':
            try:
                verification_code = session.get('verification_code')
                if datetime.datetime.now() - session.get('verification_code_time') <= 2 * 60:
                    res = make_response(
                        {'res': False, 'context': '验证码已发送,请查看邮箱确认。（INFO：两分钟冷却时间）'})
                    return res
            except Exception as r:
                pass
            verification_code = generate_verification_code()
            session['verification_code'] = verification_code
            session['verification_code_time'] = datetime.datetime.now()
            send_message(_message=f"验证码为： {verification_code}。")
            res = make_response({'res': False, 'context': '验证码已发送。'})
            return res
        else:
            verification_code = session.get('verification_code')
            if remote_verification_code == verification_code:
                res = make_response(
                    {'res': True, 'data': {'configData': config_dict, 'logData': {}}})
                session['admin'] = True
                current_app.logger.info(
                    f'- NET - {request.remote_addr} - {request.full_path} - {res.status_code} - {True}')
                return res
            else:
                res = make_response({'res': False, 'context': '验证码错误。'})
                current_app.logger.info(
                    f'- NET - {request.remote_addr} - {request.full_path} - {res.status_code} - {False}')
                return res

    @app.route(_API + '/testadmin', methods=['GET', 'POST'])
    def testconfig():
        print(session)
        try:
            if session.get('admin') or session.get('token'):
                res = make_response(
                    {'res': True, 'data': {'configData': config_dict, 'logData': {}}})
                return res
        except Exception as r:
            pass
        res = make_response({'res': False, 'context': 'no session'})
        return res

    @app.route(_API + '/updateconfig', methods=['GET', 'POST'])
    def updateconfig():
        try:
            if session.get('admin') or session.get('token'):
                new_all_config = request.json['newconfig']
                config_dict.update(new_all_config)
                with open('config/allconfig.json', 'w', encoding='utf-8') as f:
                    json.dump(config_dict, f, indent=3)
                res = make_response({'res': True})
                return res
        except Exception as r:
            pass
        res = make_response({'res': False, 'context': 'no session'})
        return res

    @app.route(_API + '/rootredirect', methods=['GET', 'POST'])
    def rootredirect():
        return config_dict['rootredirect']['where']

    # -------------------------------------------------------------------------------------------------------- #

    initScmRoute(app)
    initCmsRoute(app)
    initVideoRoute(app)

    # -------------------------------------------------------------------------------------------------------- #

    @app.route(_API + "/set_cookie")
    def set_cookie():
        resp = make_response("success")
        '''
            设置cookie,默认有效期是临时cookie,浏览器关闭就失效
            可以通过 max_age 设置有效期， 单位是秒
        '''''
        resp.set_cookie("Itcast_1", "python_1")
        resp.set_cookie("Itcast_2", "python_2")
        resp.set_cookie("Itcast_3", "python_3", max_age=3600)
        return resp

    @app.route('/test')
    def test():
        test_list = [os.path.splitext(file)[0] for file in os.listdir(r'./templates/test') if
                     os.path.splitext(file)[1] == '.html']
        test_list.remove('index')
        return render_template('test/index.html', test_list=test_list)

    @app.route('/test/<test_name>')
    def test_child(test_name):
        return render_template('test/' + test_name + '.html')

    @app.route('/fish')
    def fish():
        return render_template('templates/other/fish.html')

    @app.route('/algo')
    def algo():
        return render_template('algo/algo.html')

    @app.route('/login2')
    def _login():
        page = '''
        <form action="[[ url_for('do_login') ]]" method="post">
            <p>name: <input type="text" name="user_name" /></p>
            <p>password: <input type="text" name="test" /></p>
            <input type="submit" value="Submit" />
        </form>
        '''
        return render_template_string(page)

    @app.route('/do_login', methods=['POST'])
    def do_login():
        name = request.form.get('user_name')
        test = request.form.get('test')
        session['user_name'] = name
        session['test'] = test
        return 'success'

    @app.route('/show')
    def show():
        return session.get('user_name') + session.get('test')

    @app.route('/logout')
    def logout():
        session.pop('user_name', None)
        session.pop('test', None)
        return redirect(url_for('login2'))

    # -------------------------------------------------------------------------------------------------------- #

    # 交给vue处理
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def home(path):
        ip = request.remote_addr
        method = request.method
        res = make_response(render_template('index.html'))
        current_app.logger.info(f'- NET - {request.remote_addr} - {request.method} - {request.full_path} - {res.status_code} -')
        return res

    # -------------------------------------------------------------------------------------------------------- #

    @app.before_request
    def before():
        """
        针对app实例定义全局拦截器
        """
        url = request.full_path
        ip = request.remote_addr
        method = request.method
        current_app.logger.info(f'- NET-before - {request.remote_addr} - {request.method} - {request.full_path} -')
        if method not in ["GET", "POST"]:
            res = make_response('GUN', 403)
            return res
        elif request.remote_addr in [""]:
            res = make_response('GUN', 403)
            return res
        else:
            pass
        if url == '/sess':
            pass
        # elif session.get('is_login', '') != 'true':
        #     return '你还没有登录'
        else:
            pass