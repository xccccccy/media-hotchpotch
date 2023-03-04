import json
import os

from flask import current_app, make_response, request, Response, session

_API = '/api'

config_dict = {}
if not os.path.exists('config/allconfig.json'):
    with open('config/allconfigtemplate.json', 'r', encoding='utf-8') as f:
        config_dict = json.load(f)
    with open('config/allconfig.json', 'w', encoding='utf-8') as f:
        json.dump(config_dict, f, indent=3)
else:
    with open('config/allconfig.json', 'r', encoding='utf-8') as f:
        config_dict = json.load(f)

def initConfigRoute(app):

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
