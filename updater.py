#!/usr/bin/env python3
from git import Repo, GitCommandError
import subprocess, signal

def kill_all_process():
    p = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
    out, err = p.communicate()

    for line in out.splitlines():
        line = str(line)
        if 'receiver.py' in line or 'manage.py' in line or 'sender.py' in line or 'homebridge' in line:
            pid = int(line.split()[1])
            os.kill(pid, signal.SIGKILL)


if __name__ == "__main__":
    try:
        g = Repo('.').git
        res = g.pull()
        if res != 'Already up to date.':
            print('updated:   :D\n%s' % res)
            kill_all_process()
            subprocess.call(['/home/pi/BMS-Core/watch'])
    except GitCommandError as exp:
        print('pull exception. because: %s' % exp)
