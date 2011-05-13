from fabric.api import local, run, env

env.hosts = ['mccutchen@overloaded.org']

def deploy():
    run('cd strftime.org && git pull --rebase')
