import requests

request_session = requests.session()
home_url = 'https://api.github.com/repos/xccccccy'

def getRepos(repos):
    resp = request_session.get(f"{home_url}/{repos}", headers={'Authorization':token, 'accept': 'application/vnd.github+json'}, timeout=5)
    temp = resp.json()
    
    return temp