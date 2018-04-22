import io
import os
import sys
import contextlib
import subprocess
import shutil
import json

import requests
from git import Repo


ERROR_MSG = 'Please provide a namespace and a repo name in the payload!'
WEB_URL = 'http://165.227.188.115'


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = io.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


def get_stdin():
    buf = ''
    for line in sys.stdin:
        buf = buf + line
    return buf


def main():
    try:
        payload = json.loads(get_stdin())
        namespace = payload['repository']['owner']['login']
        repo_name = payload['repository']['name']
        url = f'https://github.com/{namespace}/{repo_name}'
    except Exception as e:
        print(ERROR_MSG)
        raise
    try:
        shutil.rmtree(f'./tmp/{repo_name}', ignore_errors=True)
        Repo.clone_from(url, f'./tmp/{repo_name}')
    except Exception as e:
        print(e)
        raise
    with stdoutIO() as std_out:
        try:
            p1 = subprocess.Popen(
                ['python3', f'tmp/{repo_name}/test.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            p2 = p1.stdout.read().decode('utf-8')
            p3 = p1.stderr.read().decode('utf-8')
            status = False
            if len(p2) > 0:
                print(p2)
            else:
                print(p3)
                if 'failures' not in p3:
                    status = True
            payload = {
                'repo_name': repo_name,
                'status': status

            }
            r = requests.put(f'{WEB_URL}/projects/update', json=payload)
            print(json.dumps(r.json()))
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
