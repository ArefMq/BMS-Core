#!/usr/bin/env python
from git import Repo, GitCommandError

g = Repo('.').git

if __name__ == "__main__":
    try:
        res = g.pull()
        if res != 'Already up to date.':
            print('updated:   :D\n%s' % res)
    except GitCommandError as exp:
        print('pull exception. because: %s' % exp)
