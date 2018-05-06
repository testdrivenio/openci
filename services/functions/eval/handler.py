import io
import os
import sys
import contextlib
import subprocess
import shutil

from git import Repo


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = io.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


def main():
    try:
        shutil.rmtree('./tmp', ignore_errors=True)
        Repo.clone_from(
            'https://github.com/testdrivenio/pycon-sample', './tmp')
    except Exception as e:
        print(e)
        raise
    with stdoutIO() as std_out:
        try:
            p1 = subprocess.Popen(
                ['python3', 'tmp/test.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            p2 = p1.stdout.read().decode('utf-8')
            p3 = p1.stderr.read().decode('utf-8')
            if len(p2) > 0:
                print(p2)
            else:
                print(p3)
        except Exception as e:
            print(e)
    print(std_out.getvalue())


if __name__ == '__main__':
    main()
