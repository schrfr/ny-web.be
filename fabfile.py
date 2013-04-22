from fabric.api import run, cd, env, prefix


def host():
    env.hosts = ['user@domain:port']
    env.path = '/home/constant/www/reader.lgru.net/www/run/'


def deploy():
    with cd(env.path):
        run('git pull origin master')

        with prefix('source /home/constant/www/reader.lgru.net/venv/bin/activate'):
            run('python manage.py collectstatic --noinput')

    run('touch /home/constant/www/reader.lgru.net/wsgi.py') 
