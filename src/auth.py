import requests


def auth(site,user_name,pass_word):
    (u,p) = (user_name,pass_word)
    r = requests.post(site + "/sessions/current", data={"username":'sa@maxmoney.com',"password" : 'MaxMoney@2016'},
                      verify=False, auth=('maxmoney','maxmoney@@1'))
    if r.status_code == 200:
        return r.json().get('session')
    if r.status_code == 201:
        return auth()
    print r.status_code
    print r.content
