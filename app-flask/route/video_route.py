from flask import current_app, make_response, request, Response, render_template, render_template_string, url_for, redirect, session
from database import dbop

_VIDEOAPI = '/videoapi'

def initVideoRoute(app):
    @app.route(_VIDEOAPI + '/search', methods=['GET', 'POST'])
    def videoSearch():
        searchString = request.json['s']
        if searchString:
            return make_response(dbop.searchVideo(searchString))
        else:
            return make_response('NO', 404)