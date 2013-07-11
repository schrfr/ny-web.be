from fabric.api import run, cd, env, prefix


env.hosts = ['ny-ny@ny-web.be']
env.path = '/home/ny-ny/apps/ny/'


def deploy():
    with cd(env.path):
        run('git pull origin master')
    run('/home/ny-ny/init/ny restart') 
