#!/usr/bin/env python
from git import Repo, GitCommandError

g = Repo('.').git


def kill_all_process():
    for line in out.splitlines():
    line = str(line)
    if 'receiver.py' in line or 'manage.py' in line or 'sender.py' in line:
        pid = int(line.split()[1])
        os.kill(pid, signal.SIGKILL)



if __name__ == "__main__":
    try:
        res = g.pull()
        if res != 'Already up to date.':
            print('updated:   :D\n%s' % res)
    except GitCommandError as exp:
        print('pull exception. because: %s' % exp)
