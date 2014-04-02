"""
Generic fabfile for my "static" web sites hosted on TextDrive. Knows how to
bootstrap and deploy those sites.

Assumptions:
 * We're operating in a directory with the same name as the web site
 * The github repo for the site has the same name as well
"""

from fabric.api import env, local, run, task

env.hosts = ['mccutch.org']
env.use_ssh_config = True


TARGET_DIR = '/var/www/strftime.org'


@task
def ensure_target():
    run('mkdir -p {}'.format(TARGET_DIR))


@task
def deploy():
    """Build and deploy a new version of the site."""
    build()
    src = 'dist/'
    dst = '{}:{}'.format(env.hosts[0], TARGET_DIR)
    if not dst.endswith('/'):
        dst = dst + '/'
    cmd = 'rsync --verbose --progress --recursive --delete {} {}'.format(
        src, dst)
    local(cmd)
    clean()


@task
def build():
    """Build a new index.html page from the Python docs."""
    clean()
    local('cp -r resources dist')
    local('./build.py > dist/index.html')


@task
def clean():
    """Clean up after a build."""
    local('rm -rf dist')
