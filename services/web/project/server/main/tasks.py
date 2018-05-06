# project/server/main/tasks.py


import json

import requests


def create_task(project_url, openfass_url):
    url_list = project_url.split('/')
    payload = {
        'namespace': url_list[3],
        'repo_name': url_list[4]
    }
    url = f'{openfass_url}:8080/function/func_eval'
    headers = {'Content-Type': 'text/plain'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    data = r.json()
    return data
