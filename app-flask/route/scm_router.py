from flask import current_app, make_response, request, Response, render_template, render_template_string, url_for, redirect, session
import requests
import json
import sys
import os


request_session = requests.session()
_SCMAPI = '/scmapi'
home_url = 'https://api.github.com/repos/xccccccy'

def initScmRoute(app):

    @app.route(_SCMAPI + '/set/token', methods=['GET', 'POST'])
    def setToken():
        token = request.json['token']
        resp =  _check_token(token)
        if resp.status_code // 100 == 2:
            if resp.json()['id'] == 97515896:
                session['token'] = token
                return make_response('success')
            else:
                return make_response('NO', 404)
        else:
            return make_response(resp.json()['message'], resp.status_code)

    @app.route(_SCMAPI + '/test/token', methods=['GET', 'POST'])
    def testToken():
        if session.get('token'):
            return make_response('success')
        else:
            return make_response('NO SCM TOKEN!', 404)

    version_dict = {}
    with open('scm/version.json', 'r', encoding='utf-8') as f:
        version_dict = json.load(f)

    @app.route(_SCMAPI + '/get/allReposInfo', methods=['GET', 'POST'])
    def getReposInfo():
        if not get_token():
            print('not token')
            return make_response('NO', 403)
        return make_response(version_dict)

    @app.route(_SCMAPI + '/get/allversioninfo', methods=['GET', 'POST'])
    def getAllVersionInfo():
        if not get_token():
            print('not token')
            return make_response('NO', 403)
        repos = request.json['repos']
        data = {
            "version_historys" : getVersionHistorys(repos),
            "now_version": version_dict[repos]['now_version']
        }
        return make_response(data)

    @app.route(_SCMAPI + '/update/fastversion', methods=['GET', 'POST'])
    def updateFastVersionapi():
        if not get_token():
            print('not token')
            return make_response('NO', 403)
        appName = request.json['app']
        print(appName)
        if appName == 'My Wrold':
            os.system("git checkout develop")
            os.system("git pull")
            os.chdir('../book-vue3')
            os.system("git checkout develop")
            os.system("git pull")
            os.system("npm run build")
            os.chdir('../flask-vue-myworld')
            print(os.getcwd())
            return make_response('success')
        return make_response('NO', 404)


    @app.route(_SCMAPI + '/update/version', methods=['GET', 'POST'])
    def updateVersionapi():
        if not get_token():
            print('not token')
            return make_response('NO', 403)
        repos = request.json['repos']
        version = request.json['version']
        if repos in version_dict.keys():
            version_dict[repos]['now_version'] = version
            updateVersion(repos, version)
            with open('scm/version.json', 'w', encoding='utf-8') as f:
                json.dump(version_dict, f, indent=3)
            print(os.getcwd())
            if repos == "flask-vue-myworld":
                os.system("git pull")
                os.system("git checkout alpha/" + version[1:])
            else:
                os.chdir('../' + repos)
                os.system("git pull")
                os.system("git checkout alpha/" + version[1:])
                print(os.getcwd())
                os.chdir('../flask-vue-myworld')
                print(os.getcwd())
            return make_response('sucess')
        return make_response("Don't exist repos or don't exist version.", 404)

    @app.route(_SCMAPI + '/new/version', methods=['GET', 'POST'])
    def newVersion():
        if not get_token():
            print('not token')
            return make_response('NO', 403)
        repos = request.json['repos']
        commitSha = request.json['commitSha']
        version = request.json['version']
        mode = request.json['mode']
        if mode == 'new':
            resp = _new_reference(repos, commitSha, version)
            if resp.status_code // 100 == 2:
                return make_response('success')
            else:
                return make_response(resp.json()['message'], resp.status_code)
        else:
            resp = _update_reference(repos, commitSha, version)
            if resp.status_code // 100 == 2:
                return make_response('success')
            else:
                return make_response(resp.json()['message'], resp.status_code)

    @app.route(_SCMAPI + '/get/<repos>', methods=['GET', 'POST'])
    def get_repos(repos):
        if not get_token():
            print('not token')
            return make_response('NO', 403)
        token = get_token()
        resp = request_session.get(f"{home_url}/{repos}", headers={'Authorization':token, 'accept': 'application/vnd.github+json'}, timeout=5)
        temp = check_404(resp)
        if temp:
            res = make_response({'data': temp})
        else:
            res = make_response('NO', 404)
        return res

    @app.route(_SCMAPI + '/get/<repos>/branches', methods=['GET', 'POST'])
    def get_branches(repos):
        if not get_token():
            print('not token')
            return make_response('NO', 403)
        temp = _get_branches(repos)
        if temp:
            res = make_response({'data': temp})
        else:
            res = make_response('NO', 404)
        return res
    
    @app.route(_SCMAPI + '/get/<repos>/branches/<branch>', methods=['GET', 'POST'])
    def get_branche(repos, branch):
        if not get_token():
            print('not token')
            return make_response('NO', 403)
        temp = _get_branche(repos, branch)
        if temp:
            res = make_response({'data': temp})
        else:
            res = make_response('NO', 404)
        return res

    @app.route(_SCMAPI + '/get/<repos>/commits', methods=['GET', 'POST'])
    def get_commits(repos):
        if not get_token():
            print('not token')
            return make_response('NO', 403)
        temp = _get_commits(repos)
        if temp:
            res = make_response({'data': temp})
        else:
            res = make_response('NO', 404)
        return res

    @app.route(_SCMAPI + '/get/<repos>/releases', methods=['GET', 'POST'])
    def get_releases(repos):
        if not get_token():
            print('not token')
            return make_response('NO', 403)
        temp = _get_releases(repos)
        if temp:
            res = make_response({'data': temp})
        else:
            res = make_response('NO', 404)
        return res
    
    def check_404(resp):
        if resp.status_code // 100 == 2 or resp.status_code == 304:
            return resp.json()
        else:
            return None

    def get_token():
        if isDebug():
            return session.get('token') if session.get('token') else ""
        else:
            return session.get('token')

    def _get_branches(repos):
        token = get_token()
        resp = request_session.get(f"{home_url}/{repos}/branches", headers={'Authorization':token, 'accept': 'application/vnd.github+json'}, timeout=5)
        return check_404(resp)
    
    def _get_branche(repos, branch):
        token = get_token()
        resp = request_session.get(f"{home_url}/{repos}/branches/{branch}", headers={'Authorization':token, 'accept': 'application/vnd.github+json'}, timeout=5)
        return check_404(resp)

    def _new_reference(repos, commitSha, version):
        token = get_token()
        if version and version[0] == 'v' or version[0] == 'V':
            pass
        else:
            return None
        data = {
            'ref': 'refs/heads/alpha/' + version[1:],
            'sha': commitSha
        }
        resp = request_session.post(f"{home_url}/{repos}/git/refs", json=data, headers={'Authorization':token, 'accept': 'application/vnd.github+json'}, timeout=5)
        return resp

    def _update_reference(repos, commitSha, version):
        token = get_token()
        data = {
            'forceboolean': True,
            'sha': commitSha
        }
        resp = request_session.patch(f"{home_url}/{repos}/git/refs/heads/alpha/{ version[1:] }", json=data, headers={'Authorization':token, 'accept': 'application/vnd.github+json'}, timeout=5)
        return resp

    def _get_commits(repos):
        token = get_token()
        resp = request_session.get(f"{home_url}/{repos}/commits", headers={'Authorization':token, 'accept': 'application/vnd.github+json'}, timeout=5)
        return check_404(resp)

    def _get_releases(repos):
        token = get_token()
        resp = request_session.get(f"{home_url}/{repos}/releases", headers={'Authorization':token, 'accept': 'application/vnd.github+json'}, timeout=5)
        return check_404(resp)

    def _check_token(token):
        resp = request_session.get(f"https://api.github.com/user", headers={'Authorization':token, 'accept': 'application/vnd.github+json'}, timeout=5)
        return resp

    def getVersionHistorys(repos):
        all_branch = _get_branches(repos)
        all_branch = all_branch if all_branch else []
        branches = [branch['name'] for branch in all_branch if branch['name'].startswith('alpha/')]
        version_historys = {}
        for branch in branches:
            temp = _get_branche(repos, branch)
            version_historys[branch] =  temp if temp else {}
        return version_historys

def updateVersion(repos, version):
    print(repos, version)
    print('Debug: ', isDebug())
    if isDebug():
        pass
    else:
        pass

def isDebug():
    if len(sys.argv) > 1:
        return True
    return False