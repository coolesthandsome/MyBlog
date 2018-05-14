# -*- coding: utf-8 -*-

from fabric.api import env,run
from fabric.operations import sudo

GIT_REPO="https://github.com/coolesthandsome/MyBlog.git"

env.user='colin'
env.password='mrfeng064924'

env.hosts=['149.28.142.149']

env.port='22'

def deploy():
    source_folder='/home/colin/sites/blog.colinfeng.com/MyBlog/blogproject'

    run('cd %s && git pull' % source_folder)
    run("""cd {} &&
    /home/colin/sites/blog.colinfeng.com/env/bin/pip install -r requirements.txt &&
    /home/colin/sites/blog.colinfeng.com/env/bin/python3 manage.py collectstatic --noinput &&
    /home/colin/sites/blog.colinfeng.com/env/bin/python3 manage.py migrate
    """.format(source_folder))

    sudo('restart gunicorn-blog.colinfeng.com')
    sudo('service nginx reload')
