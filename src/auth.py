import requests
import c


def auth():
    (u,p) = (c.web_server_user,c.web_server_password)
    r = requests.post(c.site + "/sessions/current", data=c.credentials, verify=False, auth=(u,p))
    if r.status_code == 200:
        return r.json().get('session')
    if r.status_code == 201:
        return auth()
    print r.status_code
    print r.content
    raise 'Auth Failure'