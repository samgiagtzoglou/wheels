from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.api import local

env.hosts = ['root@107.170.61.201']

def deploy():
    code_dir = '/var/www/env/wheels'
    with cd(code_dir):
        run("git pull")
        # run("touch app.wsgi")