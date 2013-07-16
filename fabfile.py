from fabric.api import run, cd, env, local


env.hosts = ['ny-ny@ny-web.be']
env.path = '/home/ny-ny/apps/ny/'

def getdb():
    with cd(env.path):
        local('/usr/bin/scp ny-ny@ny-web.be:/home/ny-ny/apps/ny/ny/ny.db ny/')

def deploy():
    with cd(env.path):
        run('git pull origin master')
        run('/home/ny-ny/venv/bin/python manage.py collectstatic --noinput')
        run('/home/ny-ny/init/ny restart') 
