import json
import os

from flask import current_app, make_response, request, Response, session
from face_recognize import face_recognize_component
from database import dbop

from .config_route import config_dict

_FACEAPI = '/faceapi'

def initFaceRoute(app):

    @app.route(_FACEAPI + '/facerecognition', methods=['GET', 'POST'])
    def api_face_recognize():  # 考虑同步问题
        if not config_dict['openLogin']['if']:
            return make_response({'res': False, 'context': '已经关闭登录功能！', 'type': False})
        if not config_dict['openFacerecognize']['if']:
            return make_response({'res': False, 'context': '已经关闭人脸登录功能！', 'type': False})
        img_base64 = request.json['img_base64'].split(',')[1]
        hasface, face_id = face_recognize_component.recognize(img_base64)
        if not face_id:
            res = Response(json.dumps({'res': False, 'hasface': hasface}), mimetype='application/json')
        else:
            user = dbop.queryUser(face_id)['user']
            res = Response(json.dumps({'res': True, 'id': face_id, 'name': user['name'], 'icon':user['icon']}), mimetype='application/json')
        face_id = face_id if face_id else 'None'
        current_app.logger.info(f'- NET - {request.remote_addr} - {request.full_path} - {res.status_code} - {face_id}')
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
        res = Response(json.dumps({'res': res_add_face}), mimetype='application/json')
        current_app.logger.info(f'- NET - {request.remote_addr} - {request.full_path} - {res.status_code} - {face_id} - {res_add_face}')
        return res